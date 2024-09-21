from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def detect_anomalies(data):
    """
    Detects anomalies in the preprocessed network traffic data using the IsolationForest algorithm.

    Parameters:
    data (pandas.DataFrame): The preprocessed network traffic data.

    Returns:
    pandas.DataFrame: A DataFrame containing the detected anomalies.
    """
    # Convert IP addresses to numeric form
    data['src_ip'] = data['src_ip'].apply(lambda x: int(x.replace('.', '')))
    data['dst_ip'] = data['dst_ip'].apply(lambda x: int(x.replace('.', '')))
    
    # Encode the 'protocol' column to numerical values
    label_encoder = LabelEncoder()
    data['protocol'] = label_encoder.fit_transform(data['protocol'])
    
    # Create and fit the IsolationForest model
    model = IsolationForest(contamination=0.01)
    model.fit(data)
    
    # Predict anomalies
    predictions = model.predict(data)
    anomalies = data[predictions == -1]
    return anomalies