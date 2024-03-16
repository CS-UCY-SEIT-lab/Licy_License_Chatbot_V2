from flask import Flask, render_template, jsonify, request
import os
import asyncio
import json
from flask_cors import CORS
from License import License
from BeginnerTree import BeginnerTree
from BasicTree import BasicTree
import requests


def read_beginner_questions(filepath, licenses):
    options = []
    option_explanations = []

    with open(filepath, "r") as file:
        data = json.load(file)

    # Extract the arrays from the JSON data
    questions = data["questions"]
    question_explanations = data["question_explanations"]
    options = data["options"]
    option_explanations = data["option_explanations"]
    option_license_subsets = data["option_license_subset"]
    option_paths = data["option_paths"]

    # restrictions = data["restrictions"]
    # categories = data["categories"]

    return (
        questions,
        question_explanations,
        options,
        option_explanations,
        option_license_subsets,
        option_paths,
    )


def read_file_paths():
    config_file_path = "../file paths/filepaths.json"

    with open(config_file_path, "r") as config_file:
        config_data = json.load(config_file)

    return {
        "questions_file": config_data["questions_file"],
        "licenses_folder": config_data["licenses_folder"],
        "dependencies_file": config_data["dependencies_file"],
        "templates_folder": config_data["templates_folder"],
        "static_folder": config_data["static_folder"],
    }


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)

    return files


def extract_data(parsed_data):
    answer = ""
    info = None
    print("Parsed data", parsed_data)
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

    print("Answer", answer)
    print("Info", info)
    return answer, info


def read_licenses(folder_path):
    licenses = []
    filenames = list_files_in_directory(folder_path)
    for filename in filenames:
        with open(folder_path + filename, "r") as file:
            data = json.load(file)

        title = data["title"]
        spdx_id = data["spdx-id"]
        description = data["description"]
        permissions = data["permissions"]
        conditions = data["conditions"]
        limitations = data["limitations"]

        license = License()
        license.set_info(
            conditions, limitations, permissions, title, description, spdx_id
        )
        licenses.append(license)

    return licenses


# run : rasa run actions & rasa run --enable-api --cors="*" --port 5005 --debug & python ./backend/chatbot.py

app = Flask(__name__, template_folder="../UI/templates", static_folder="../UI/static")
CORS(app)


@app.route("/")
def index():
    return render_template("website_test.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_answer = data.get("user_input")
    url = "http://localhost:5005/webhooks/rest/webhook"
    data = {"sender": "User", "message": user_answer}
    answer = ""
    action_json = "None"
    response = requests.post(url, json=data)

    if response.status_code == 200:
        parsed_data = response.json()

        answer, action_json = extract_data(parsed_data)
        # print(action_json)

        return jsonify({"message": answer, "info": action_json})

    return jsonify({"message": "Error"})


# Suggest me some licenses that allow modifications and require document-changes and  don't offer liability
if __name__ == "__main__":
    app.run(debug=True)
