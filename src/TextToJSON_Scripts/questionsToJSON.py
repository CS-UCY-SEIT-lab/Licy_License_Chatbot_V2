import json


def question_to_json(question_file, output_json):
    key_questions = {}
    questions = []
    keys = []

    with open(question_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.strip():
            parts = line.split("|")
            key_questions[parts[1][len(" key: ") :].strip()] = parts[0].strip()

    for key, value in key_questions.items():
        questions.append(value)
        keys.append(key)

    instance_data = {
        "questions": questions,
        "keys": keys,
    }

    json_data = json.dumps(instance_data, indent=2)

    # Write JSON data to a file
    with open(output_json, "w") as json_file:
        json_file.write(json_data)


question_to_json(
    "../Chatbot Questions/chatbot_questions.txt",
    "../Chatbot Questions/questions_json.json",
)
