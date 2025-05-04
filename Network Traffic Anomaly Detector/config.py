# Configuration settings
PACKET_COUNT = 100  # Number of packets to capture
ISOLATION_FOREST_CONTAMINATION = 0.01  # Contamination parameter for IsolationForest

# Email configuration for alerts
EMAIL_CONFIG = {
    'sender_email': 'your_email@example.com',
    'receiver_email': 'recipient@example.com',
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'smtp_username': 'your_email@example.com',
    'smtp_password': 'your_password'
}

# Alert system configuration
ALERT_CONFIG = {
    # Enable/disable different alert methods
    'terminal': True,     # Print to terminal
    'email': False,       # Send email alerts
    'slack': False,       # Send Slack notifications
    'file': True,         # Save alerts to file

    # Slack webhook URL (if Slack alerts are enabled)
    'slack_webhook_url': '',

    # Minimum severity level for alerts (LOW, MEDIUM, HIGH, CRITICAL)
    'min_severity': 'MEDIUM',

    # Custom email recipients for different severity levels
    'severity_recipients': {
        'HIGH': ['security-team@example.com'],
        'CRITICAL': ['security-team@example.com', 'sysadmin@example.com', 'ciso@example.com']
    }
}
