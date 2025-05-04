from scapy.all import sniff
# Import the configuration variable for packet count
from config import PACKET_COUNT

def capture_packets(count=PACKET_COUNT, iface=None, timeout=10):
    """
    Captures network packets using the scapy library.

    Parameters:
    count (int): The number of packets to capture. Defaults to PACKET_COUNT from config.
    iface (str, optional): The network interface to sniff on. Defaults to None (scapy's default).
    timeout (int, optional): The time in seconds to wait for packets. Defaults to 10.

    Returns:
    list: A list of captured packets. Returns an empty list if no packets are captured within the timeout.
    """
    print(f"[*] Starting packet capture (count={count}, timeout={timeout}s, interface={iface if iface else 'default'})...")
    try:
        # Use the configured count, interface, and timeout
        packets = sniff(count=count, iface=iface, timeout=timeout)
        print(f"[*] Captured {len(packets)} packets.")
        return packets
    except PermissionError:
        print("[!] Permission denied. Please run the script with root/administrator privileges for packet capture.")
        return []
    except Exception as e:
        print(f"[!] An error occurred during packet capture: {e}")
        return []

# Example of how it might be called (for testing purposes, not part of the main logic)
# if __name__ == "__main__":
#     # You might need to run this script with sudo/administrator privileges
#     # packets = capture_packets(count=50, iface='eth0', timeout=5) # Specify interface
#     packets = capture_packets() # Use default config values
#     if packets:
#         print(f"Successfully captured {len(packets)} packets.")
#         # You could add code here to process or display packets if needed
#     else:
#         print("No packets captured or an error occurred.")
