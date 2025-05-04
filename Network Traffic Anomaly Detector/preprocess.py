# type: ignore # Ignore type checking for the entire file due to Scapy/Pandas type issues
from scapy.all import IP, TCP, UDP, ICMP, Packet
import pandas as pd
from typing import List, Dict, Any

def preprocess_packets(packets: List[Packet]) -> pd.DataFrame:
    """
    Preprocesses a list of network packets to extract relevant features and returns a DataFrame.

    Parameters:
    packets (List[scapy.packet.Packet]): A list of captured network packets.

    Returns:
    pandas.DataFrame: A DataFrame containing the extracted features for packets that could be processed.
                      Returns an empty DataFrame if the input list is empty or no packets could be processed.
    """
    processed_data_list: List[Dict[str, Any]] = []

    print(f"[*] Preprocessing {len(packets)} packets...")

    for packet in packets:
        features: Dict[str, Any] = {}

        # Add timestamp (useful for time-based analysis later)
        features['timestamp'] = packet.time

        # Check for IP layer
        if IP in packet:
            features['src_ip'] = packet[IP].src
            features['dst_ip'] = packet[IP].dst
            features['length'] = len(packet)
            features['protocol_num'] = packet[IP].proto # Store protocol number

            # Check for Transport Layer (TCP, UDP, ICMP)
            if TCP in packet:
                features['protocol'] = 'TCP'
                features['src_port'] = packet[TCP].sport
                features['dst_port'] = packet[TCP].dport
                # Add TCP flags (optional but useful)
                features['tcp_flags'] = packet[TCP].flags
            elif UDP in packet:
                features['protocol'] = 'UDP'
                features['src_port'] = packet[UDP].sport
                features['dst_port'] = packet[UDP].dport
                features['tcp_flags'] = None # No TCP flags for UDP
            elif ICMP in packet:
                features['protocol'] = 'ICMP'
                features['icmp_type'] = packet[ICMP].type
                features['icmp_code'] = packet[ICMP].code
                features['src_port'] = None # No ports for ICMP
                features['dst_port'] = None
                features['tcp_flags'] = None
            else:
                # Handle other IP protocols or packets without a common transport layer
                features['protocol'] = f'Other_IP({packet[IP].proto})'
                features['src_port'] = None
                features['dst_port'] = None
                features['tcp_flags'] = None
        else:
            # Handle non-IP packets (e.g., ARP)
            features['src_ip'] = None
            features['dst_ip'] = None
            features['length'] = len(packet)
            features['protocol_num'] = None
            features['protocol'] = packet.summary().split()[0] if packet.summary() else 'Non-IP' # Basic attempt to get protocol name
            features['src_port'] = None
            features['dst_port'] = None
            features['tcp_flags'] = None


        # Add the extracted features to our list
        processed_data_list.append(features)

    # Convert the list of dictionaries into a pandas DataFrame
    if not processed_data_list:
        print("[*] No packets could be processed into features.")
        # Return an empty DataFrame with expected columns even if no data
        # type: ignore # Ignore type checking here due to Pyright/Pandas stub issue
        return pd.DataFrame(columns=['timestamp', 'src_ip', 'dst_ip', 'length', 'protocol_num',
                                     'protocol', 'src_port', 'dst_port', 'tcp_flags'])


    df = pd.DataFrame(processed_data_list)

    # Optional: Basic data type conversion after creating DataFrame
    # This can help ensure numeric types are correct, especially for ports and length
    # df['length'] = pd.to_numeric(df['length'], errors='coerce')
    # df['src_port'] = pd.to_numeric(df['src_port'], errors='coerce')
    # df['dst_port'] = pd.to_numeric(df['dst_port'], errors='coerce')


    print(f"[*] Finished preprocessing. Created DataFrame with {len(df)} rows.")
    return df

# Example of how it might be used (for testing)
# if __name__ == "__main__":
#     # This part requires capturing packets, so it's better to test via main.py
#     # from scapy.all import IP, TCP, UDP, Ether
#     # # Create some dummy packets
#     # packets = [
#     #     Ether()/IP(src='192.168.1.1', dst='8.8.8.8')/TCP(sport=12345, dport=80, flags='S'),
#     #     Ether()/IP(src='192.168.1.2', dst='8.8.8.8')/UDP(sport=54321, dport=53),
#     #     Ether()/IP(src='8.8.8.8', dst='192.168.1.1')/ICMP(type=8, code=0),
#     #     Ether()/IP(src='192.168.1.3', dst='1.1.1.1') # IP packet without transport layer
#     # ]
#     # df = preprocess_packets(packets)
#     # print(df)
