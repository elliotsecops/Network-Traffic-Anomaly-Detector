def send_alerts(anomalies):
    if not anomalies.empty:
        print("Anomalies detected:\n", anomalies)
    else:
        print("No anomalies detected.")
