import pandas as pd

# Load predicted traffic data
csv_file = "C:/Users/tx682/traffic-simulation/predicted_traffic.csv"
df = pd.read_csv(csv_file)

# Count occurrences of benign and malicious traffic
report = df["prediction"].value_counts()

# Save summary to a text file with UTF-8 encoding
report_filename = "C:/Users/tx682/traffic-simulation/detection_report.txt"
with open(report_filename, "w", encoding="utf-8") as file:
    file.write("📊 Intrusion Detection Summary Report\n")
    file.write("------------------------------------\n")
    file.write(f"Total Entries: {len(df)}\n")
    file.write(f"Benign Traffic: {report.get('benign', 0)}\n")
    file.write(f"Malicious Traffic: {report.get('malicious', 0)}\n")

print(f"✅ Report Generated: {report_filename}")
