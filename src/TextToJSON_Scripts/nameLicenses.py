import os
import json
import random


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)

    return files


intent_text = [
    "I want to know more about ",
    "Give me some info on ",
    "What do you know about ",
    "Have you heard about ",
]


def read_licenses_info(folder_path):
    titles = []
    ids = []
    descriptions = []
    permissions = []
    conditions = []
    limitations = []
    filenames = list_files_in_directory(folder_path)
    for filename in filenames:
        with open(folder_path + filename, "r") as file:
            data = json.load(file)

        titles.append(data["title"])
        ids.append(data["spdx-id"])
        descriptions.append(data["description"])
        permissions.append(data["permissions"])
        conditions.append(data["conditions"])
        limitations.append(data["limitations"])

    return titles, ids


def writeLicensesNames():
    licenses, ids = read_licenses_info("../licensesJSON/")
    with open("licenses.txt", "w") as file:
        for license in licenses:
            file.write(
                "- "
                + random.choice(intent_text)
                + '"['
                + license
                + '](license_name)" \n'
            )


def writeLicensesIds():
    licenses, ids = read_licenses_info("../licensesJSON/")
    with open("licenses.txt", "w") as file:
        for id in ids:
            file.write(
                "- " + random.choice(intent_text) + '"[' + id + '](license_name)" \n'
            )


# writeLicensesNames()
writeLicensesIds()
