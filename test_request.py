import requests

url = "http://127.0.0.1:5000/predict"
data = {"text": "Car accident due to overspeeding in rainy weather"}
response = requests.post(url, json=data)

print(response.json())  # Expected output: {'Predicted Cluster': 2}
