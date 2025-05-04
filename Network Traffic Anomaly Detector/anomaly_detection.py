from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import pandas as pd
# Import the configuration variable
from config import ISOLATION_FOREST_CONTAMINATION

def detect_anomalies(data):
    """
    Detects anomalies in the preprocessed network traffic data using the IsolationForest algorithm.

    Parameters:
    data (pandas.DataFrame): The preprocessed network traffic data.

    Returns:
    pandas.DataFrame: A DataFrame containing the detected anomalies.
    """
    # Make a copy to avoid modifying the original DataFrame in place if it's used elsewhere
    processed_data = data.copy()

    # Convert IP addresses to numeric form (Note: This is a basic conversion, consider alternatives for better representation)
    # Ensure columns exist before attempting to transform
    if 'src_ip' in processed_data.columns:
        processed_data['src_ip'] = processed_data['src_ip'].apply(lambda x: int(x.replace('.', '')) if isinstance(x, str) else x)
    if 'dst_ip' in processed_data.columns:
        processed_data['dst_ip'] = processed_data['dst_ip'].apply(lambda x: int(x.replace('.', '')) if isinstance(x, str) else x)

    # Encode the 'protocol' column to numerical values
    # Ensure column exists and handle potential non-string types
    if 'protocol' in processed_data.columns:
        # Convert to string first to handle potential NaN or other types
        processed_data['protocol'] = processed_data['protocol'].astype(str)
        label_encoder = LabelEncoder()
        processed_data['protocol'] = label_encoder.fit_transform(processed_data['protocol'])

    # Select only numeric columns for the model
    # This is a safer approach than using all columns
    numeric_data = processed_data.select_dtypes(include=['number'])

    # Check if there's any numeric data to process
    if numeric_data.empty:
        print("Warning: No numeric data available for anomaly detection after preprocessing.")
        return pd.DataFrame(columns=data.columns) # Return empty DataFrame with original columns

    # Create and fit the IsolationForest model
    # Use the contamination value from config.py
    # NOTE: This trains the model on the current batch of data, which is not ideal
    # for detecting anomalies in *new* data. A better approach is to train on
    # normal data separately and use the trained model here for prediction only.
    try:
        model = IsolationForest(contamination=ISOLATION_FOREST_CONTAMINATION, random_state=42) # Added random_state for reproducibility
        model.fit(numeric_data) # type: ignore # Ignore potential type errors here - data is expected to be numeric

        # Predict anomalies
        predictions = model.predict(numeric_data)

        # Filter the original data based on predictions
        # Need to align predictions back to the original index
        anomalies_indices = numeric_data.index[predictions == -1]
        anomalies = data.loc[anomalies_indices]

        return anomalies
    except Exception as e:
        print(f"Error during anomaly detection: {e}")
        return pd.DataFrame(columns=data.columns) # Return empty DataFrame on error
