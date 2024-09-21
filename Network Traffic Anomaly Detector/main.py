from capture import capture_packets
from preprocess import preprocess_data
from anomaly_detection import detect_anomalies
from alerts import send_alerts
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='anomaly_detection.log', level=logging.INFO)

def main():
    logging.info("Starting packet capture...")
    packets = capture_packets(count=100)
    logging.info(f"Captured {len(packets)} packets.")
    
    data = [preprocess_data(packet) for packet in packets if preprocess_data(packet) is not None]
    df = pd.DataFrame(data)
    
    anomalies = detect_anomalies(df)
    logging.info(f"Detected {len(anomalies)} anomalies.")
    
    send_alerts(anomalies)

if __name__ == "__main__":
    main()