import requests


def extract_data(parsed_data):

    answer = ""

    info = None

    print(parsed_data)

    for dictionary in parsed_data:

        if "text" in dictionary:

            answer += dictionary["text"]

        elif "custom" in dictionary:

            info = dictionary["custom"]

            if info["key"] == "start-tutorial":

                info = {
                    "key": "start-tutorial",
                    "options": ["Beginner", "Have knowledge"],
                }

    return answer, info


url = "http://localhost:5005/webhooks/rest/webhook"

data = {"sender": "User", "message": "Hello"}

response = requests.post(url, json=data)

if response.status_code == 200:
    parsed_data = response.json()
    answer, action_json = extract_data(parsed_data)
    print("Response: ", response.json())

else:

    print("StATUS CODE:", response.status_code)

    print("Error")
