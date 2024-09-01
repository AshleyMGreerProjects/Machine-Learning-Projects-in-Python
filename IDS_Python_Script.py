import argparse
from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime
import logging
from twilio.rest import Client
import os

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'your_twilio_phone_number')
MY_PHONE_NUMBER = '520-414-1025'

# Initialize logging
logging.basicConfig(filename="ids_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Thresholds
SYN_FLOOD_THRESHOLD = 100  # SYN flood detection threshold
PORT_SCAN_THRESHOLD = 10    # Port scan detection threshold
BLACKLIST_THRESHOLD = 200   # Threshold to blacklist an IP
UDP_FLOOD_THRESHOLD = 100   # UDP flood detection threshold

# Data structures to keep track of packet counts
syn_count = {}
scan_count = {}
udp_count = {}
blacklist = set()

def send_sms_alert(message):
    """Send an SMS alert using Twilio."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=MY_PHONE_NUMBER
    )

def detect_syn_flood(packet):
    """Detect SYN flood attacks."""
    if packet.haslayer(TCP) and packet[TCP].flags == 'S':
        src_ip = packet[IP].src

        if src_ip in blacklist:
            return

        syn_count[src_ip] = syn_count.get(src_ip, 0) + 1

        if syn_count[src_ip] > SYN_FLOOD_THRESHOLD:
            alert = f"Potential SYN Flood Attack Detected from {src_ip}"
            print(alert)
            logging.warning(alert)
            send_sms_alert(alert)
            blacklist_ip(src_ip)

def detect_port_scan(packet):
    """Detect port scanning."""
    if packet.haslayer(TCP):
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport

        if src_ip in blacklist:
            return

        scan_count[(src_ip, dst_port)] = scan_count.get((src_ip, dst_port), 0) + 1

        if len([port for (ip, port) in scan_count if ip == src_ip]) > PORT_SCAN_THRESHOLD:
            alert = f"Potential Port Scan Detected from {src_ip}"
            print(alert)
            logging.warning(alert)
            send_sms_alert(alert)
            blacklist_ip(src_ip)

def detect_udp_flood(packet):
    """Detect UDP flood attacks."""
    if packet.haslayer(UDP):
        src_ip = packet[IP].src

        if src_ip in blacklist:
            return

        udp_count[src_ip] = udp_count.get(src_ip, 0) + 1

        if udp_count[src_ip] > UDP_FLOOD_THRESHOLD:
            alert = f"Potential UDP Flood Attack Detected from {src_ip}"
            print(alert)
            logging.warning(alert)
            send_sms_alert(alert)
            blacklist_ip(src_ip)

def blacklist_ip(ip):
    """Add an IP address to the blacklist."""
    if ip in syn_count and syn_count[ip] > BLACKLIST_THRESHOLD:
        alert = f"Blacklisting IP: {ip} due to excessive malicious activity."
        print(alert)
        logging.warning(alert)
        send_sms_alert(alert)
        blacklist.add(ip)

def packet_callback(packet):
    """Callback function for each packet."""
    if packet.haslayer(IP):
        detect_syn_flood(packet)
        detect_port_scan(packet)
        detect_udp_flood(packet)

def main():
    parser = argparse.ArgumentParser(description="Simple Intrusion Detection System")
    parser.add_argument("-i", "--interface", type=str, required=True, help="Network interface to sniff on (e.g., eth0)")
    parser.add_argument("--syn_threshold", type=int, default=SYN_FLOOD_THRESHOLD, help="SYN flood threshold")
    parser.add_argument("--scan_threshold", type=int, default=PORT_SCAN_THRESHOLD, help="Port scan threshold")
    parser.add_argument("--blacklist_threshold", type=int, default=BLACKLIST_THRESHOLD, help="IP blacklist threshold")
    parser.add_argument("--udp_threshold", type=int, default=UDP_FLOOD_THRESHOLD, help="UDP flood threshold")
    args = parser.parse_args()

    global SYN_FLOOD_THRESHOLD, PORT_SCAN_THRESHOLD, BLACKLIST_THRESHOLD, UDP_FLOOD_THRESHOLD
    SYN_FLOOD_THRESHOLD = args.syn_threshold
    PORT_SCAN_THRESHOLD = args.scan_threshold
    BLACKLIST_THRESHOLD = args.blacklist_threshold
    UDP_FLOOD_THRESHOLD = args.udp_threshold

    print("Starting Intrusion Detection System...")
    print(f"Sniffing on interface: {args.interface}")

    sniff(iface=args.interface, prn=packet_callback, store=0)

if __name__ == "__main__":
    main()
