from scapy.all import IP, TCP

def preprocess_data(packet):
    """
    Preprocesses a network packet to extract relevant features.

    Parameters:
    packet (scapy.packet.Packet): The network packet to preprocess.

    Returns:
    dict: A dictionary containing the extracted features if the packet contains IP and TCP layers, otherwise None.
    """
    if IP in packet and TCP in packet:
        features = {
            'src_ip': packet[IP].src,
            'dst_ip': packet[IP].dst,
            'src_port': packet[TCP].sport,
            'dst_port': packet[TCP].dport,
            'length': len(packet),
            'protocol': 'TCP'
        }
        return features
    return None