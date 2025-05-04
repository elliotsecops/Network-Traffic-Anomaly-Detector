import smtplib
import logging
import json
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import EMAIL_CONFIG

# En lugar de configurar el logging con basicConfig, solo obtenemos una instancia de logger
logger = logging.getLogger(__name__)

# Definir niveles de severidad para las alertas
SEVERITY_LEVELS = {
    'LOW': 0,
    'MEDIUM': 1,
    'HIGH': 2,
    'CRITICAL': 3
}

class AlertManager:
    """Clase para manejar diferentes tipos de alertas y notificaciones"""

    def __init__(self, config=None):
        """
        Inicializa el gestor de alertas

        Args:
            config (dict, optional): Configuración personalizada para el gestor de alertas
        """
        self.config = config if config else {}

        # Configurar métodos de alerta habilitados (por defecto, terminal siempre habilitada)
        self.alert_methods = {
            'terminal': True,  # Siempre habilitado
            'email': self._is_email_configured(),
            'slack': 'slack_webhook_url' in self.config and self.config['slack_webhook_url'],
            'file': True,  # Siempre habilitado
        }

        # Directorio para almacenar alertas como JSON
        self.alerts_dir = os.path.join('logs', 'alerts')
        os.makedirs(self.alerts_dir, exist_ok=True)

        logger.info(f"Alert Manager initialized with methods: {', '.join([k for k, v in self.alert_methods.items() if v])}")

    def _is_email_configured(self):
        """Verifica si la configuración de correo electrónico es válida"""
        required_fields = ['sender_email', 'receiver_email', 'smtp_server', 'smtp_port']
        default_values = ['your_email@example.com', 'recipient@example.com', 'smtp.example.com']

        # Verificar que todos los campos requeridos existen
        if not all(field in EMAIL_CONFIG for field in required_fields):
            return False

        # Verificar que no son valores por defecto
        for field in required_fields:
            if field in EMAIL_CONFIG and EMAIL_CONFIG[field] in default_values:
                return False

        return True

    def send_alert(self, anomalies, severity='MEDIUM'):
        """
        Envía alertas por todos los métodos configurados

        Args:
            anomalies (DataFrame): DataFrame con las anomalías detectadas
            severity (str): Nivel de severidad de la alerta (LOW, MEDIUM, HIGH, CRITICAL)
        """
        if anomalies.empty:
            logger.info("No anomalies detected, no alerts sent.")
            return

        # Validar nivel de severidad
        if severity not in SEVERITY_LEVELS:
            severity = 'MEDIUM'

        # Generar el contenido de la alerta
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert_title = f"ALERT [{severity}]: {len(anomalies)} network anomalies detected at {timestamp}"

        # Convertir anomalías a formato legible
        anomalies_str = anomalies.to_string(index=False)

        # Enviar por métodos habilitados
        methods_used = []

        # Alerta por terminal
        if self.alert_methods['terminal']:
            self._send_terminal_alert(alert_title, anomalies)
            methods_used.append('terminal')

        # Alerta por correo electrónico
        if self.alert_methods['email']:
            success = self._send_email_alert(alert_title, anomalies_str, severity)
            if success:
                methods_used.append('email')

        # Alerta por Slack
        if self.alert_methods['slack']:
            success = self._send_slack_alert(alert_title, anomalies_str, severity)
            if success:
                methods_used.append('slack')

        # Guardar alerta en archivo
        if self.alert_methods['file']:
            self._save_alert_to_file(alert_title, anomalies, severity)
            methods_used.append('file')

        logger.info(f"Alert sent using methods: {', '.join(methods_used)}")

    def _send_terminal_alert(self, title, anomalies):
        """Imprime la alerta en la terminal"""
        print("\n" + "="*80)
        print(title)
        print("="*80)
        print("Anomalies detected:")
        print(anomalies)
        print("="*80 + "\n")
        return True

    def _send_email_alert(self, title, content, severity):
        """
        Envía una alerta por correo electrónico

        Args:
            title (str): Título de la alerta
            content (str): Contenido detallado de la alerta
            severity (str): Nivel de severidad

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Crear mensaje
            message = MIMEMultipart()
            message["From"] = EMAIL_CONFIG['sender_email']

            # Seleccionar destinatarios según la severidad si están configurados
            recipients = EMAIL_CONFIG['receiver_email']
            if self.config and 'severity_recipients' in self.config:
                if severity in self.config['severity_recipients'] and self.config['severity_recipients'][severity]:
                    recipients = ', '.join(self.config['severity_recipients'][severity])

            message["To"] = recipients
            message["Subject"] = title

            # Crear contenido HTML con formato
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .severity-{severity.lower()} {{
                        background-color: {self._get_severity_color(severity)};
                        color: white;
                        padding: 5px 10px;
                        border-radius: 3px;
                    }}
                    pre {{
                        background-color: #f5f5f5;
                        padding: 10px;
                        border-radius: 5px;
                        overflow-x: auto;
                    }}
                </style>
            </head>
            <body>
                <h2>{title}</h2>
                <p>Severity: <span class="severity-{severity.lower()}">{severity}</span></p>
                <p>The Network Traffic Anomaly Detector has identified unusual traffic patterns that may indicate security issues.</p>
                <h3>Detected Anomalies:</h3>
                <pre>{content}</pre>
                <p>Please investigate these anomalies promptly.</p>
                <hr>
                <p><small>This is an automated alert from the Network Traffic Anomaly Detector.</small></p>
            </body>
            </html>
            """

            # Adjuntar contenido al mensaje
            message.attach(MIMEText(html, "html"))

            # Conectar al servidor SMTP y enviar correo
            with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                server.starttls()  # Iniciar TLS
                # Autenticar si hay credenciales
                if 'smtp_username' in EMAIL_CONFIG and 'smtp_password' in EMAIL_CONFIG:
                    if EMAIL_CONFIG['smtp_username'] and EMAIL_CONFIG['smtp_password']:
                        server.login(EMAIL_CONFIG['smtp_username'], EMAIL_CONFIG['smtp_password'])

                # Enviar correo
                server.sendmail(
                    EMAIL_CONFIG['sender_email'],
                    recipients.split(', ') if isinstance(recipients, str) else recipients,
                    message.as_string()
                )

            logger.info(f"Email alert sent to {recipients}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

    def _send_slack_alert(self, title, content, severity):
        """
        Envía una alerta a Slack

        Args:
            title (str): Título de la alerta
            content (str): Contenido detallado de la alerta
            severity (str): Nivel de severidad

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        if 'slack_webhook_url' not in self.config or not self.config['slack_webhook_url']:
            logger.warning("Slack webhook URL not configured")
            return False

        try:
            # Formatear el contenido como un código en Slack
            slack_content = f"```\n{content}\n```"

            # Determinar el color según la severidad
            color = self._get_severity_color(severity, slack=True)

            # Crear payload para Slack
            payload = {
                "attachments": [
                    {
                        "fallback": title,
                        "color": color,
                        "title": title,
                        "text": slack_content,
                        "footer": "Network Traffic Anomaly Detector",
                        "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }

            # Enviar a Slack
            response = requests.post(
                self.config['slack_webhook_url'],
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                logger.info("Slack alert sent successfully")
                return True
            else:
                logger.error(f"Failed to send Slack alert: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False

    def _save_alert_to_file(self, title, anomalies, severity):
        """
        Guarda la alerta en un archivo JSON

        Args:
            title (str): Título de la alerta
            anomalies (DataFrame): DataFrame con las anomalías
            severity (str): Nivel de severidad
        """
        try:
            # Crear estructura para guardar
            timestamp = datetime.now()
            alert_data = {
                "title": title,
                "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "severity": severity,
                "anomalies": json.loads(anomalies.to_json(orient='records'))
            }

            # Nombre de archivo basado en timestamp
            filename = os.path.join(
                self.alerts_dir,
                f"alert_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            )

            # Guardar a archivo
            with open(filename, 'w') as f:
                json.dump(alert_data, f, indent=2)

            logger.info(f"Alert saved to file: {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to save alert to file: {e}")
            return False

    def _get_severity_color(self, severity, slack=False):
        """
        Devuelve el color asociado al nivel de severidad

        Args:
            severity (str): Nivel de severidad
            slack (bool): Si es True, devuelve colores para Slack

        Returns:
            str: Color en formato hexadecimal o nombre de color para Slack
        """
        colors = {
            'LOW': '#4CAF50' if not slack else 'good',           # Verde
            'MEDIUM': '#FFC107' if not slack else 'warning',     # Amarillo
            'HIGH': '#FF9800' if not slack else 'danger',        # Naranja
            'CRITICAL': '#F44336' if not slack else 'danger',    # Rojo
        }

        return colors.get(severity, colors['MEDIUM'])

    def update_config(self, new_config):
        """
        Actualiza la configuración del gestor de alertas

        Args:
            new_config (dict): Nueva configuración
        """
        self.config.update(new_config)

        # Actualizar métodos habilitados
        if 'email' in new_config:
            self.alert_methods['email'] = new_config['email']
        else:
            self.alert_methods['email'] = self._is_email_configured()

        if 'slack_webhook_url' in new_config:
            self.alert_methods['slack'] = bool(new_config['slack_webhook_url'])

        if 'terminal' in new_config:
            self.alert_methods['terminal'] = new_config['terminal']

        if 'file' in new_config:
            self.alert_methods['file'] = new_config['file']

        logger.info(f"Alert Manager configuration updated. Methods: {', '.join([k for k, v in self.alert_methods.items() if v])}")

# Función de compatibilidad con la versión anterior
def send_alert(anomalies):
    """
    Función para mantener compatibilidad con el código antiguo

    Args:
        anomalies (DataFrame): DataFrame con las anomalías detectadas
    """
    # Crear instancia de AlertManager con configuración por defecto
    alert_manager = AlertManager()

    # Determinar severidad basada en número de anomalías
    if anomalies.empty:
        severity = 'LOW'
    else:
        num_anomalies = len(anomalies)
        if num_anomalies <= 1:
            severity = 'LOW'
        elif num_anomalies <= 3:
            severity = 'MEDIUM'
        elif num_anomalies <= 5:
            severity = 'HIGH'
        else:
            severity = 'CRITICAL'

    # Enviar alerta
    alert_manager.send_alert(anomalies, severity)
