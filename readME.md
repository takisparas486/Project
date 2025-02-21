# **Intrusion Detection System (IDS) - Complete Project Guide**

## **📌 Overview**
This project implements an AI-powered **Intrusion Detection System (IDS)** using **Dockerized traffic simulation** and **Machine Learning**. The IDS detects malicious network activities such as **Port Scanning, DDoS Attacks, and SQL Injections**.

---

## **🚀 Project Steps**

### **1️⃣ Setup Environment**
#### **📌 Install Required Tools**
- Install **Docker & Docker Compose**
- Install **Wireshark & TShark**
- Install **Python 3 & Dependencies**

#### **📌 Check Installation**
```powershell
docker --version
docker-compose --version
tshark -v
python --version
```

---

### **2️⃣ Create and Run Dockerized Traffic Simulation**
#### **📌 Create `docker-compose.yml`**
```yaml
version: '3.8'
services:
  frontend:
    image: node:latest
    container_name: frontend
    working_dir: /app
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    command: ["sh", "-c", "npm install && npm start"]

  apache:
    image: httpd:latest
    container_name: apache-server
    ports:
      - "8080:80"
    volumes:
      - ./apache/www:/usr/local/apache2/htdocs

  db:
    image: postgres:latest
    container_name: database
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

#### **📌 Run Docker Containers**
```powershell
docker-compose up -d
```

#### **📌 Verify Running Containers**
```powershell
docker ps
```

---

### **3️⃣ Simulate Normal (Benign) Traffic**
#### **📌 Create `benign_traffic.py`**
```python
import requests
import time

URL = "http://localhost:8080"
for i in range(20):
    response = requests.get(URL)
    print(f"Request {i+1}: {response.status_code}")
    time.sleep(0.5)
```
#### **📌 Run Traffic Simulation**
```powershell
python benign_traffic.py
```

#### **📌 Capture Benign Traffic**
```powershell
docker run --rm -v ${PWD}:/pcap --net=host nicolaka/netshoot tcpdump -i eth0 -w /pcap/benign_traffic.pcap
```

---

### **4️⃣ Simulate Malicious Attacks & Capture Traffic**
#### **📌 Create `all_attacks.py` (Runs All Attacks at Once)**
```python
import os
import threading
import requests
import socket
import time

TARGET_IP = "127.0.0.1"
TARGET_PORT = 80

# Function for Port Scanning Attack
def port_scan():
    for port in range(1, 1001):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((TARGET_IP, port))
        if result == 0:
            print(f"Port {port} is open!")
        s.close()

# Function for DDoS Attack
def ddos_attack():
    while True:
        try:
            requests.get(f"http://{TARGET_IP}:{TARGET_PORT}")
        except:
            pass

# Function for SQL Injection Attack
def sql_injection():
    url = "http://localhost:8080/login.php"
    payload = {"user": "admin' OR 1=1 --", "password": "password"}
    requests.get(url, params=payload)

# Run Attacks in Threads
threading.Thread(target=port_scan).start()
threading.Thread(target=ddos_attack).start()
threading.Thread(target=sql_injection).start()
```
```powershell
python all_attacks.py
```

#### **📌 Capture Malicious Traffic**
```powershell
docker run --rm -v ${PWD}:/pcap --net=host nicolaka/netshoot tcpdump -i eth0 -w /pcap/malicious_traffic.pcap
```

---

### **5️⃣ Process Traffic Data for AI Model**
#### **📌 Convert `.pcap` to `.csv` (TShark)**
```powershell
tshark -r malicious_traffic.pcap -T fields -E separator=/t -E header=y -E quote=n -E occurrence=f -e frame.time -e ip.src -e ip.dst -e ip.proto -e frame.len -e tcp.flags -e udp.length > traffic_data.tsv
```
#### **📌 Convert `.tsv` to `.csv` (Python)**
```python
import pandas as pd
df = pd.read_csv("traffic_data.tsv", sep="\t", encoding="utf-8")
df.to_csv("traffic_data.csv", index=False)
```
```powershell
python convert_tsv_to_csv.py
```

#### **📌 Label the Data**
```python
malicious_ips = {"port_scan": ["192.168.65.7"], "ddos": ["192.168.65.8"], "sql_injection": ["192.168.65.9"]}
def assign_label(row):
    return next((f"malicious-{attack}" for attack, ips in malicious_ips.items() if row["ip.src"] in ips), "benign")
df["label"] = df.apply(assign_label, axis=1)
df.to_csv("traffic_data_labeled.csv", index=False)
```
```powershell
python label_data.py
```

---

### **6️⃣ Train Machine Learning Model**
```powershell
python train_model.py
```

---

### **7️⃣ Detect New Intrusions**
```powershell
python detect_intrusions.py
```

---

### **🎯 Summary**
✅ **Simulated and captured network traffic**  
✅ **Labeled data and trained AI model**  
✅ **Successfully detected attacks using ML**  
🚀 **Now ready for real-time intrusion detection!**  
