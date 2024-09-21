from scapy.all import sniff, IP, TCP

def capture_packets(count=100):
    """
    Captures network packets using the scapy library.

    Parameters:
    count (int): The number of packets to capture. Default is 100.

    Returns:
    list: A list of captured packets.
    """
    return sniff(count=count)