import pandas as pd
import re

# Define file paths
csv_file = "C:/Users/tx682/traffic-simulation/traffic_data_utf8.csv"
cleaned_csv_file = "C:/Users/tx682/traffic-simulation/traffic_data_cleaned.csv"

# Load CSV while fixing encoding
df = pd.read_csv(csv_file, encoding="utf-8")

# Fix corrupted column names
df.rename(columns=lambda x: x.encode('latin1').decode('utf-8'), inplace=True)

# Standardize column names (remove extra spaces, lowercase)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Fix specific column name if corrupted
if "Ã¿Ã¾frame.time" in df.columns:
    df.rename(columns={"Ã¿Ã¾frame.time": "frame_time"}, inplace=True)

# Remove "GTB Standard Time" from timestamps
if "frame_time" in df.columns:
    df["frame_time"] = df["frame_time"].apply(lambda x: re.sub(r' GTB Standard Time', '', str(x)))

# Convert TCP flags from hex to decimal
if "tcp_flags" in df.columns:
    df["tcp_flags"] = df["tcp_flags"].apply(lambda x: int(str(x), 16) if str(x).startswith("0x") else x)

# Save cleaned CSV
df.to_csv(cleaned_csv_file, index=False, encoding="utf-8")

print(f"✅ CSV Cleaning Complete! Saved as: {cleaned_csv_file}")
