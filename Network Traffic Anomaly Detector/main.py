from capture import capture_packets
# Import the new function that processes a list of packets and returns a DataFrame
from preprocess import preprocess_packets
from anomaly_detection import detect_anomalies
from alerts import AlertManager, logger as alerts_logger
import pandas as pd
import logging
import os
from config import PACKET_COUNT, ALERT_CONFIG
import sys # Import sys for geteuid check

# Crear directorio para logs si no existe
os.makedirs('logs', exist_ok=True)

# Configurar logging centralizado
# Asegúrate de que el nivel de logging sea adecuado para ver los mensajes
logging.basicConfig(
    level=logging.INFO, # Cambiado a INFO para ver mensajes informativos
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'anomaly_detector.log')),
        logging.StreamHandler()  # También mostrar logs en consola
    ]
)

# Configurar logger específico para alertas (si quieres que vaya a un archivo separado)
# Asegúrate de que el logger de alertas no tenga handlers duplicados si ya se configuró en alerts.py
# Si alerts.py ya configura su logger, esta parte podría ser redundante o necesitar ajuste.
# Por ahora, asumimos que alerts.py define 'alerts_logger' pero no configura handlers por defecto.
if not alerts_logger.handlers: # Añadir handler solo si no tiene ya uno configurado
    alerts_handler = logging.FileHandler(os.path.join('logs', 'alerts.log'))
    alerts_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    alerts_logger.addHandler(alerts_handler)
    alerts_logger.setLevel(logging.INFO) # Asegurar nivel de logging para alertas

# Obtener logger para este módulo
logger = logging.getLogger(__name__)

def determine_severity(anomalies: pd.DataFrame) -> str:
    """
    Determina el nivel de severidad basado en el número y tipo de anomalías detectadas

    Args:
        anomalies (DataFrame): DataFrame con las anomalías detectadas

    Returns:
        str: Nivel de severidad (LOW, MEDIUM, HIGH, CRITICAL)
    """
    if anomalies.empty:
        logger.info("No anomalies detected, severity is LOW.")
        return 'LOW'

    num_anomalies = len(anomalies)
    logger.info(f"Determining severity based on {num_anomalies} anomalies.")

    # Criterios avanzados de severidad (para implementación futura)
    # Aquí solo usamos el número de anomalías, pero en el futuro se podría
    # implementar lógica basada en el tipo de anomalías, puertos críticos, etc.

    if num_anomalies <= 1:
        return 'LOW'
    elif num_anomalies <= 3:
        return 'MEDIUM'
    elif num_anomalies <= 5:
        return 'HIGH'
    else:
        return 'CRITICAL'

def main():
    logger.info("Starting network anomaly detection process.")

    # Inicializar el gestor de alertas
    alert_manager = AlertManager(ALERT_CONFIG)
    logger.info("Alert manager initialized.")

    # Capturar paquetes
    logger.info(f"Starting packet capture (count={PACKET_COUNT})...")
    # capture_packets now uses the PACKET_COUNT from config internally
    # Convert the PacketList returned by capture_packets to a standard list
    packets = list(capture_packets())
    logger.info(f"Captured {len(packets)} packets.")

    # Verificar si se capturaron paquetes
    if not packets:
        logger.warning("No packets captured. Stopping analysis.")
        # Optionally send a low severity alert or log this condition
        # alert_manager.send_alert(pd.DataFrame(), 'LOW', "No packets captured.")
        return

    # Preprocesar datos
    logger.info("Starting data preprocessing...")
    # Pass the standard list of packets to the preprocessing function
    processed_df = preprocess_packets(packets)
    logger.info(f"Preprocessing finished. Resulting DataFrame has {len(processed_df)} rows.")

    # Verificar si se obtuvieron datos válidos después del preprocesamiento
    if processed_df.empty:
        logger.warning("No valid data after preprocessing. Stopping analysis.")
        # Optionally send a low severity alert or log this condition
        # alert_manager.send_alert(pd.DataFrame(), 'LOW', "No valid data after preprocessing.")
        return

    # Detectar anomalías
    logger.info("Starting anomaly detection...")
    # Pass the processed DataFrame to the anomaly detection function
    anomalies = detect_anomalies(processed_df)
    logger.info(f"Anomaly detection finished. Detected {len(anomalies)} anomalies.")

    # Determinar severidad y enviar alerta
    severity = determine_severity(anomalies)

    if not anomalies.empty:
        logger.info(f"Anomalies detected. Severity determined as: {severity}")
        alert_manager.send_alert(anomalies, severity)
    else:
        logger.info("No anomalies detected. No alert sent.")


if __name__ == "__main__":
    # Ensure running with sufficient privileges for packet capture
    # Note: os.geteuid() is Unix-specific. For Windows, you'd need a different check.
    if os.name == 'posix' and os.geteuid() != 0:
        logger.error("This script requires root privileges for packet capture on Unix-like systems.")
        # You might want to exit here or handle this differently
        # sys.exit("Please run with sudo or as administrator.")
        # For now, just log and continue, but capture_packets will likely fail
        pass # Allow execution to continue for demonstration, knowing capture will fail without root
    elif os.name == 'nt': # Basic check for Windows, though actual privilege check is more complex
         logger.warning("Running on Windows. Packet capture might require administrator privileges.")


    try:
        main()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"An unexpected error occurred during main execution: {e}", exc_info=True)
