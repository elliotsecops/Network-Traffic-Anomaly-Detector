### README.md

# Detector de Anomalías en el Tráfico de Red

Este proyecto es un detector de anomalías en el tráfico de red que captura y analiza paquetes de red para identificar comportamientos anómalos. Utiliza técnicas de aprendizaje automático para detectar desviaciones de los patrones normales de tráfico.

## Características

- **Captura de Paquetes**: Captura el tráfico de red en tiempo real utilizando `scapy`.
- **Preprocesamiento**: Prepara los datos capturados para el análisis de aprendizaje automático.
- **Detección de Anomalías**: Utiliza el algoritmo `IsolationForest` para identificar anomalías en el tráfico de red.
- **Alertas**: Imprime las anomalías detectadas en la terminal para obtener una retroalimentación inmediata.
- **Registro**: Registra todos los eventos relevantes y las anomalías detectadas en archivos de registro para un análisis futuro.
- **Docker**: El proyecto puede ejecutarse dentro de un contenedor Docker para una implementación y aislamiento fáciles.

## Estructura del Proyecto

```
Network Traffic Anomaly Detector/
│
├── alerts.py                # Lógica de alertas y notificaciones
├── anomaly_detection.log    # Archivo de registro para eventos de detección de anomalías
├── anomaly_detection.py     # Modelo de aprendizaje automático para la detección de anomalías
├── capture.py               # Lógica de captura de paquetes de red
├── config.py                # Configuración de ajustes
├── Dockerfile               # Dockerfile para la contenerización
├── logs/                    # Directorio para archivos de registro
│   └── anomaly_detector.log # Archivo de registro para el detector de anomalías
├── main.py                  # Punto de entrada principal del programa
├── preprocess.py            # Funciones de preprocesamiento de datos
├── __pycache__/             # Archivos compilados de Python (generados automáticamente)
├── requirements.txt         # Dependencias del proyecto
└── test_scapy.py            # Script de prueba para scapy
```

## Instalación

### Prerrequisitos

- Python 3.x
- Docker (opcional, para la contenerización)

### Pasos

1. **Clonar el Repositorio**:

   ```bash
   git clone https://github.com/elliotsecops/network-traffic-anomaly-detector.git
   cd network-traffic-anomaly-detector
   ```

2. **Crear y Activar un Entorno Virtual**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar Dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el Script**:

   ```bash
   sudo $(which python3) main.py
   ```

## Configuración de Docker

### Construir la Imagen de Docker

```bash
docker build -t network-traffic-anomaly-detector .
```

### Ejecutar el Contenedor de Docker

```bash
docker run --rm --net=host network-traffic-anomaly-detector
```

## Configuración

El archivo `config.py` contiene la configuración de ajustes para el proyecto, incluyendo:

- **Cantidad de Paquetes**: Número de paquetes a capturar.
- **Contaminación del Bosque de Aislamiento**: Parámetro de contaminación para el algoritmo `IsolationForest`.
- **Configuración de Correo Electrónico**: Configuración del servidor SMTP para enviar alertas por correo electrónico (actualmente deshabilitada).

## Uso

1. **Capturar Paquetes de Red**:
   El script captura el tráfico de red en tiempo real utilizando `scapy`.

2. **Preprocesar Datos**:
   Los datos capturados se preprocesan para extraer características relevantes.

3. **Detectar Anomalías**:
   El algoritmo `IsolationForest` se utiliza para detectar anomalías en el tráfico de red.

4. **Imprimir Anomalías**:
   Las anomalías detectadas se imprimen en la terminal.

5. **Registro**:
   Todos los eventos relevantes y las anomalías detectadas se registran en `logs/anomaly_detector.log`.

## Ejemplo de Salida

```bash
INFO:root:Starting packet capture...
INFO:root:Captured 100 packets.
INFO:root:Detected 1 anomalies.
Anomalies detected:
          src_ip  dst_ip  src_port  dst_port  length  protocol
30  12324998181  109604       443     57658      83         0
```

## Público Objetivo

Este proyecto es particularmente útil para los siguientes profesionales de TI:

- **Administradores de Red**: Para monitorear el tráfico de red y detectar posibles amenazas de seguridad o configuraciones incorrectas.
- **Analistas de Seguridad**: Para identificar y responder a actividades de red anómalas que podrían indicar una violación de seguridad.
- **Ingenieros de DevOps**: Para integrar el monitoreo de red en pipelines de CI/CD para una evaluación de seguridad continua.
- **Científicos de Datos**: Para analizar datos de tráfico de red y desarrollar modelos de detección de anomalías más avanzados.
- **Ingenieros de Sistemas**: Para garantizar la fiabilidad y seguridad de la infraestructura de red.

## Casos de Uso en Escenarios Reales

1. **Detección de Intrusiones**:
   - **Escenario**: Un administrador de red nota patrones de tráfico inusuales durante horas no pico.
   - **Solución**: El detector de anomalías identifica el tráfico anómalo, permitiendo al administrador investigar y mitigar posibles amenazas de seguridad.

2. **Monitoreo de Cumplimiento**:
   - **Escenario**: Una empresa necesita cumplir con los requisitos reglamentarios para el monitoreo del tráfico de red.
   - **Solución**: El detector de anomalías proporciona un monitoreo continuo y registros del tráfico de red, ayudando a la empresa a cumplir con los requisitos de cumplimiento.

3. **Solución de Problemas de Rendimiento**:
   - **Escenario**: Una red experimenta un rendimiento degradado y la causa es desconocida.
   - **Solución**: El detector de anomalías identifica patrones de tráfico inusuales que podrían estar causando los problemas de rendimiento, permitiendo al equipo de red tomar medidas correctivas.

4. **Respuesta a Incidentes de Seguridad**:
   - **Escenario**: Se detecta un incidente de seguridad y el equipo de respuesta necesita identificar rápidamente la fuente y el alcance del incidente.
   - **Solución**: El detector de anomalías proporciona alertas en tiempo real y registros del tráfico anómalo, ayudando al equipo de respuesta en sus esfuerzos de investigación y mitigación.

5. **Monitoreo Continuo en Entornos en la Nube**:
   - **Escenario**: Una aplicación basada en la nube experimenta problemas de conectividad intermitentes.
   - **Solución**: El detector de anomalías que se ejecuta en un contenedor Docker monitorea continuamente el tráfico de red, ayudando a identificar y resolver problemas de conectividad.

## Contribuciones

¡Las contribuciones son bienvenidas! No dudes en enviar un pull request o abrir un issue.

## Agradecimientos

- Gracias a las comunidades de `scapy`, `scikit-learn` y `pandas` por sus excelentes bibliotecas.
- Agradecimiento especial a todos los colaboradores y testers.

---

### README.md

# Network Traffic Anomaly Detector

This project is a network traffic anomaly detector that captures and analyzes network packets to identify anomalous behavior. It uses machine learning techniques to detect deviations from normal traffic patterns.

## Features

- **Packet Capture**: Captures real-time network traffic using `scapy`.
- **Preprocessing**: Prepares captured data for machine learning analysis.
- **Anomaly Detection**: Utilizes the `IsolationForest` algorithm to identify anomalies in network traffic.
- **Alerts**: Prints anomalies detected to the terminal for immediate feedback.
- **Logging**: Records all relevant events and detected anomalies to log files for future analysis.
- **Docker**: The project can be run inside a Docker container for easy deployment and isolation.

## Project Structure

```
Network Traffic Anomaly Detector/
│
├── alerts.py                # Alert and notification logic
├── anomaly_detection.log    # Log file for anomaly detection events
├── anomaly_detection.py     # Machine learning model for anomaly detection
├── capture.py               # Network packet capture logic
├── config.py                # Configuration settings
├── Dockerfile               # Dockerfile for containerization
├── logs/                    # Directory for log files
│   └── anomaly_detector.log # Log file for the anomaly detector
├── main.py                  # Main entry point for the program
├── preprocess.py            # Data preprocessing functions
├── __pycache__/             # Compiled Python files (automatically generated)
├── requirements.txt         # Dependencies for the project
└── test_scapy.py            # Test script for scapy
```

## Installation

### Prerequisites

- Python 3.x
- Docker (optional, for containerization)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/elliotsecops/network-traffic-anomaly-detector.git
   cd network-traffic-anomaly-detector
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**:

   ```bash
   sudo $(which python3) main.py
   ```

## Docker Setup

### Build the Docker Image

```bash
docker build -t network-traffic-anomaly-detector .
```

### Run the Docker Container

```bash
docker run --rm --net=host network-traffic-anomaly-detector
```

## Configuration

The `config.py` file contains configuration settings for the project, including:

- **Packet Count**: Number of packets to capture.
- **Isolation Forest Contamination**: Contamination parameter for the `IsolationForest` algorithm.
- **Email Configuration**: SMTP server settings for sending email alerts (currently disabled).

## Usage

1. **Capture Network Packets**:
   The script captures real-time network traffic using `scapy`.

2. **Preprocess Data**:
   Captured data is preprocessed to extract relevant features.

3. **Detect Anomalies**:
   The `IsolationForest` algorithm is used to detect anomalies in the network traffic.

4. **Print Anomalies**:
   Detected anomalies are printed to the terminal.

5. **Logging**:
   All relevant events and detected anomalies are logged to `logs/anomaly_detector.log`.

## Example Output

```bash
INFO:root:Starting packet capture...
INFO:root:Captured 100 packets.
INFO:root:Detected 1 anomalies.
Anomalies detected:
          src_ip  dst_ip  src_port  dst_port  length  protocol
30  12324998181  109604       443     57658      83         0
```

## Target Audience

This project is particularly useful for the following IT professionals:

- **Network Administrators**: To monitor network traffic and detect potential security threats or misconfigurations.
- **Security Analysts**: To identify and respond to anomalous network activities that could indicate a security breach.
- **DevOps Engineers**: To integrate network monitoring into CI/CD pipelines for continuous security assessment.
- **Data Scientists**: To analyze network traffic data and develop more advanced anomaly detection models.
- **System Engineers**: To ensure the reliability and security of network infrastructure.

## Use Cases in Real Scenarios

1. **Intrusion Detection**:
   - **Scenario**: A network administrator notices unusual traffic patterns during off-peak hours.
   - **Solution**: The anomaly detector identifies the anomalous traffic, allowing the administrator to investigate and mitigate potential security threats.

2. **Compliance Monitoring**:
   - **Scenario**: A company needs to comply with regulatory requirements for network traffic monitoring.
   - **Solution**: The anomaly detector provides continuous monitoring and logs of network traffic, helping the company meet compliance requirements.

3. **Performance Troubleshooting**:
   - **Scenario**: A network experiences degraded performance, and the cause is unknown.
   - **Solution**: The anomaly detector identifies unusual traffic patterns that could be causing the performance issues, enabling the network team to take corrective actions.

4. **Security Incident Response**:
   - **Scenario**: A security incident is detected, and the response team needs to quickly identify the source and scope of the incident.
   - **Solution**: The anomaly detector provides real-time alerts and logs of anomalous traffic, aiding the response team in their investigation and mitigation efforts.

5. **Continuous Monitoring in Cloud Environments**:
   - **Scenario**: A cloud-based application experiences intermittent connectivity issues.
   - **Solution**: The anomaly detector running in a Docker container continuously monitors network traffic, helping to identify and resolve connectivity issues.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Acknowledgments

- Thanks to the `scapy`, `scikit-learn`, and `pandas` communities for their excellent libraries.
- Special thanks to all contributors and testers.
