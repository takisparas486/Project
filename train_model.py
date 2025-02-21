import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib  # For saving the trained model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
csv_file = "C:/Users/tx682/traffic-simulation/traffic_data_labeled.csv"
df = pd.read_csv(csv_file)

# Convert labels to numeric values
df["label"] = df["label"].apply(lambda x: 1 if "malicious" in str(x) else 0)

# Convert tcp.flags from hex to decimal
if "tcp.flags" in df.columns:
    df["tcp.flags"] = df["tcp.flags"].apply(lambda x: int(str(x), 16) if str(x).startswith("0x") else int(x))

# Select features and target
features = ["frame.len", "ip.proto", "tcp.flags", "udp.length"]
X = df[features].fillna(0)  # Replace missing values
y = df["label"]

# Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Training Complete! Accuracy: {accuracy:.2f}")
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Benign", "Malicious"], yticklabels=["Benign", "Malicious"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Save trained model
model_filename = "C:/Users/tx682/traffic-simulation/intrusion_detection_model.pkl"
joblib.dump(model, model_filename)
print(f"✅ Model Saved as: {model_filename}")
