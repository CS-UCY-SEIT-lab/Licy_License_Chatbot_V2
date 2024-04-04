from flask import Flask, render_template, jsonify, request, session
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore
import os
import asyncio
import jsonpickle
import json
from flask_cors import CORS
from License import License
from BeginnerTree import BeginnerTree
from BasicTree import BasicTree
from Node import Node
import requests
import secrets
import random
import time


def generate_user_id():
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    random_number = random.randint(10000, 99999)  # Generate a random number
    user_id = f"{timestamp}{random_number}"  # Concatenate timestamp and random number
    return user_id


def read_beginner_questions(filepath):

    with open(filepath, "r") as file:
        data = json.load(file)

    # Extract the arrays from the JSON data
    questions = data["questions"]
    question_explanations = data["question_explanations"]
    options = data["options"]
    option_explanations = data["option_explanations"]
    option_license_subsets = data["option_license_subsets"]
    option_paths = data["option_paths"]
    option_colors = data["option_colors"]

    # restrictions = data["restrictions"]
    # categories = data["categories"]

    return (
        questions,
        question_explanations,
        options,
        option_explanations,
        option_license_subsets,
        option_paths,
        option_colors,
    )


def read_permissions(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    permissions = data["permissions"]
    explanations = data["permission_explanations"]

    return permissions, explanations


def read_basic_questions(filepath, licenses):
    key_questions = {}
    positive_subsets = []
    negative_subsets = []
    with open(filepath, "r") as file:
        data = json.load(file)

    # Extract the arrays from the JSON data
    questions = data["questions"]
    keys = data["keys"]
    question_explanations = data["question_explanations"]

    for i in range(len(keys)):
        key_questions[keys[i]] = questions[i]

    for key, value in key_questions.items():
        questions.append(value)
        positive_subset = []
        negative_subset = []
        for license in licenses:
            if "None" in key:
                positive_subset.append(license.id)
                negative_subset.append(license.id)
            else:
                if key.startswith("!"):
                    if license.all_rights[key[1:]]:
                        negative_subset.append(license.id)
                    else:
                        positive_subset.append(license.id)
                else:
                    if license.all_rights[key]:
                        positive_subset.append(license.id)
                    else:
                        negative_subset.append(license.id)

        positive_subsets.append(positive_subset)
        negative_subsets.append(negative_subset)

    return (
        questions,
        positive_subsets,
        negative_subsets,
        question_explanations,
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
        "basic_questions_file": config_data["basic_questions"],
        "beginner_questions_file": config_data["beginner_questions"],
        "permissions_file": config_data["permissions_file"],
    }


def get_num_nodes(file_path):
    with open(file_path, "r") as file:
        sequence = file.read()
    max_value = 0
    for line in sequence.split("\n"):
        if line:
            parts = line.split("->")
            value = int(parts[0])

            max_value = max(max_value, value)

    return max_value


def create_nodes(
    file_path, questions, positive_subsets, negative_subsets, question_explanations
):
    nodes = []
    for i in range(get_num_nodes(file_path)):
        nodes.append(Node(i + 1))

    with open(file_path, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        line_index = 0

    while line_index < len(lines):
        line1 = lines[line_index]
        line2 = lines[line_index + 1]
        line3 = lines[line_index + 2]

        # Process your two lines here
        parts1 = line1.replace(" ", "").split("->")
        parts2 = line2.replace(" ", "").split("->")
        parts3 = line3.replace(" ", "").split("->")

        node_index = int(parts1[0]) - 1
        options = ["Yes", "No"]

        if parts1[1] != "end":
            positive_node = nodes[int(parts1[1]) - 1]
        else:
            positive_node = None

        if parts2[1] != "end":
            negative_node = nodes[int(parts2[1]) - 1]
        else:
            negative_node = None

        if parts3[1] == "end":
            neutral_node = None
            options.append("Don't Care")
        elif parts3[1] == "none" or parts3[1] == "None":
            neutral_node = None
        else:
            neutral_node = nodes[int(parts3[1]) - 1]
            options.append("Don't Care")

        current_node = nodes[node_index]
        current_node.build_node(
            positive_node,
            neutral_node,
            negative_node,
            [questions[node_index]],
            positive_subsets[node_index],
            negative_subsets[node_index],
            options,
            question_explanations[node_index],
        )
        if positive_node is not None and positive_node.id > current_node.id:
            positive_node.set_parent(current_node)
            # positive_node.set_subset(positive_subsets[node_index])
        if negative_node is not None and negative_node.id > current_node.id:
            negative_node.set_parent(current_node)
            # negative_node.set_subset(negative_subsets[node_index])

        line_index = line_index + 3

    return nodes


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)

    return files


def extract_data(parsed_data):
    answer = ""
    info = None

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

paths = read_file_paths()
licenses = read_licenses(paths.get("licenses_folder"))

app = Flask(__name__, template_folder="../UI/templates", static_folder="../UI/static")
CORS(app)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def index():
    session["userID"] = generate_user_id()
    print("USER ID:", session["userID"])
    return render_template("website_test.html")


@app.route("/retrieve-license-info", methods=["POST"])
def retrieve_license_info():
    titles = []
    permissions = []
    ids = []
    requested_licenses = request.json.get("license_ids")

    for requested_license_id in requested_licenses:
        for license in licenses:
            if license.id == requested_license_id:
                titles.append(license.title)
                permissions.append(
                    [license.permissions, license.conditions, license.limitations]
                )
                ids.append(license.id)

    return jsonify(
        {
            "license_titles": titles,
            "license_permissions": permissions,
            "license_ids": ids,
        }
    )


@app.route("/start-tutorial", methods=["POST"])
def start_beginner_tutorial():
    data = request.json

    if data.get("type") == "Beginner":

        (
            questions,
            question_explanations,
            options,
            option_explanations,
            option_license_subsets,
            option_paths,
            option_colors,
        ) = read_beginner_questions("../chatbot-questions/beginner_questions.json")
        tree = BeginnerTree(
            questions,
            question_explanations,
            options,
            option_explanations,
            option_license_subsets,
            option_paths,
            option_colors,
        )

        user_snapshots = user_ref.where("userID", "==", session["userID"]).get()
        print("USER ID:", session.get("userID"))
        if len(user_snapshots) > 0:
            user_snapshots[0].reference.update({"Tree": jsonpickle.encode(tree)})
        else:
            user_ref.add({"userID": session["userID"], "Tree": jsonpickle.encode(tree)})

        current_question_data = asyncio.run(tree.start_questionnaire(request=None))

    else:
        (
            questions,
            positive_subsets,
            negative_subsets,
            question_explanations,
        ) = read_basic_questions(paths.get("basic_questions_file"), licenses)

        nodes = create_nodes(
            paths.get("dependencies_file"),
            questions,
            positive_subsets,
            negative_subsets,
            question_explanations,
        )

        tree = BasicTree(
            nodes,
            nodes[0],
            set(positive_subsets[0]).union(set(negative_subsets[0])),
        )
        print("USER ID:", session.get("userID"))
        user_snapshots = user_ref.where("userID", "==", session["userID"]).get()

        if len(user_snapshots) > 0:
            user_snapshots[0].reference.update({"Tree": jsonpickle.encode(tree)})
        else:
            user_ref.add({"userID": session["userID"], "Tree": jsonpickle.encode(tree)})

        current_question_data = asyncio.run(tree.start_questionnaire(request=None))

    return jsonify(current_question_data)


@app.route("/questionnaire", methods=["POST"])
def questionnaire():
    user_snapshot = user_ref.where("userID", "==", session["userID"]).get()[0]
    tree = jsonpickle.decode(user_snapshot.to_dict()["Tree"])
    user_request = request.json

    current_question_data = asyncio.run(
        tree.start_questionnaire(request=user_request.get("answer"))
    )
    user_snapshot.reference.update({"Tree": jsonpickle.encode(tree)})
    return jsonify(current_question_data)


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

        return jsonify({"message": answer, "info": action_json})

    return jsonify({"message": "Error"})


@app.route("/chatbot-info", methods=["POST"])
def get_chatbot_info():
    permissions, explanations = read_permissions(paths.get("permissions_file"))
    license_titles = [license.title for license in licenses]
    license_ids = [license.id for license in licenses]

    return jsonify(
        {
            "permissions": permissions,
            "permission_explanations": explanations,
            "license_titles": license_titles,
            "license_ids": license_ids,
        }
    )


# Suggest me some licenses that allow modifications and require document-changes and  don't offer liability
if __name__ == "__main__":
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    user_ref = db.collection("users")
    app.run(debug=True)
