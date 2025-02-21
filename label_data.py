import pandas as pd

# Load dataset
csv_file = "C:/Users/tx682/traffic-simulation/traffic_data_cleaned.csv"
labeled_csv_file = "C:/Users/tx682/traffic-simulation/traffic_data_labeled.csv"

df = pd.read_csv(csv_file)

# Define Malicious IPs (based on attack scripts)
malicious_ips = {
    "port_scan": ["192.168.65.7"],   # Nmap Port Scanning
    "ddos": ["192.168.65.8"],        # DDoS Attack
    "sql_injection": ["192.168.65.9"] # SQL Injection
}

# Create label column
def assign_label(row):
    src_ip = row["ip.src"]
    dst_ip = row["ip.dst"]

    # Check if source IP is malicious
    for attack, ip_list in malicious_ips.items():
        if src_ip in ip_list:
            return f"malicious-{attack}"

    # If not in malicious list, it's benign
    return "benign"

df["label"] = df.apply(assign_label, axis=1)

# Save new CSV
df.to_csv(labeled_csv_file, index=False)

print(f"✅ Labeling Complete! Saved as: {labeled_csv_file}")
