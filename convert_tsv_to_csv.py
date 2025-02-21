import pandas as pd

# Define file paths
tsv_file = "C:/Users/tx682/traffic-simulation/traffic_data.tsv"
clean_tsv_file = "C:/Users/tx682/traffic-simulation/traffic_data_cleaned.tsv"
csv_file = "C:/Users/tx682/traffic-simulation/traffic_data.csv"

# Step 1: Remove NULL bytes from the file
with open(tsv_file, "rb") as infile, open(clean_tsv_file, "wb") as outfile:
    for line in infile:
        outfile.write(line.replace(b"\x00", b""))  # Remove NULL bytes

print("✅ NULL bytes removed. Processing cleaned TSV file...")

# Step 2: Load cleaned TSV file and convert to CSV
try:
    df = pd.read_csv(clean_tsv_file, sep="\t", encoding="utf-8", engine="c")
except UnicodeDecodeError:
    print("⚠️ UnicodeDecodeError detected. Retrying with 'ISO-8859-1' encoding...")
    df = pd.read_csv(clean_tsv_file, sep="\t", encoding="ISO-8859-1", engine="c")

# Save as CSV
df.to_csv(csv_file, index=False)

print(f"✅ Conversion Complete! CSV saved as: {csv_file}")
