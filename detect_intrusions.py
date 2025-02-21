import pandas as pd
import joblib
import numpy as np

# Load the trained model
model_filename = "C:/Users/tx682/traffic-simulation/intrusion_detection_model.pkl"
model = joblib.load(model_filename)

# Load new traffic data (assuming it's saved as `new_traffic.csv`)
new_csv_file = "C:/Users/tx682/traffic-simulation/new_traffic.csv"
df_new = pd.read_csv(new_csv_file)

# Function to convert tcp.flags from hex to decimal, handling missing values
def convert_tcp_flags(value):
    if pd.isna(value) or value == "-" or value == "":
        return 0  # Default value for missing flags
    try:
        return int(str(value), 16) if str(value).startswith("0x") else int(value)
    except ValueError:
        return 0  # If conversion fails, return 0

# Function to convert udp.length to numeric (handling '-')
def convert_udp_length(value):
    if pd.isna(value) or value == "-" or value == "":
        return 0  # Default value for missing length
    try:
        return int(value)
    except ValueError:
        return 0  # If conversion fails, return 0

# Apply conversion functions
if "tcp.flags" in df_new.columns:
    df_new["tcp.flags"] = df_new["tcp.flags"].apply(convert_tcp_flags)

if "udp.length" in df_new.columns:
    df_new["udp.length"] = df_new["udp.length"].apply(convert_udp_length)

# Select relevant features
features = ["frame.len", "ip.proto", "tcp.flags", "udp.length"]
X_new = df_new[features].fillna(0).astype(float)  # Convert all to float

# Make predictions
predictions = model.predict(X_new)

# Add predictions to dataframe
df_new["prediction"] = ["malicious" if p == 1 else "benign" for p in predictions]

# Save results
predicted_csv = "C:/Users/tx682/traffic-simulation/predicted_traffic.csv"
df_new.to_csv(predicted_csv, index=False)

print(f"✅ Intrusion Detection Complete! Results saved as: {predicted_csv}")
