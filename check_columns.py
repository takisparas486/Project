import pandas as pd

csv_file = "C:/Users/tx682/traffic-simulation/traffic_data_cleaned.csv"

# Load CSV and print column names
df = pd.read_csv(csv_file, encoding="utf-8")
print("✅ Detected Columns:", df.columns.tolist())
