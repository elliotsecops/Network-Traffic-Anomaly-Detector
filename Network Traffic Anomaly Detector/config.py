# Configuration settings
PACKET_COUNT = 100  # Number of packets to capture
ISOLATION_FOREST_CONTAMINATION = 0.01  # Contamination parameter for IsolationForest

# Email configuration for alerts
EMAIL_CONFIG = {
    'sender_email': 'your_email@example.com',
    'receiver_email': 'recipient@example.com',
    'smtp_server': 'smtp.example.com',  # Correct SMTP server address
    'smtp_port': 587,  # Correct SMTP server port
    'smtp_username': 'your_email@example.com',
    'smtp_password': 'your_password'
}