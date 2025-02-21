import requests
import time

URL = "http://localhost:8080"

for i in range(1000):
    try:
        response = requests.get(URL)
        print(f"Request {i+1}: {response.status_code}")
        time.sleep(0.5)  # Simulate user browsing every 0.5 seconds
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
