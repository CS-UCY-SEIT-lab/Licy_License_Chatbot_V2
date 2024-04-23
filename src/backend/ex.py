import requests

url = "http://localhost:5005/webhooks/rest/webhook"
data = {"sender": "User", "message": "Hello"}
response = requests.post(url, json=data)
if response.status_code == 200:
    print("Response: ", response.json())
else:
    print("StATUS CODE:", response.status_code)
    print("Error")
