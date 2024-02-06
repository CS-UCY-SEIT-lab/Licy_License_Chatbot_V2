import os
import json


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)

    return files


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
        # ids.append(data["spdx-id"])
        # descriptions.append(data["description"])
        # permissions.append(data["permissions"])
        # conditions.append(data["conditions"])
        # limitations.append(data["limitations"])

    return titles


def writeLicenses():
    licenses = read_licenses_info("../licensesJSON/")
    with open("licenses.txt", "w") as file:
        for license in licenses:
            file.write("- " + license + "\n")


writeLicenses()
