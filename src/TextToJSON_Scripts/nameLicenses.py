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
    "What is",
    "",
]
negative_positive = [
    "do ",
    "does ",
    "isn't ",
    "aren't ",
    "doesn't ",
    "",
    "",
    "don't ",
    "dont ",
    "doesnt ",
    "",
    "do not ",
    "does not ",
    "",
    "",
]
key_permissions = {
    (
        "permit",
        "allow",
        "accept",
        "forbid",
    ): [
        "commercial-use",
        "modifications",
        "distribution",
        "private-use",
        "sublicensing",
        "patent-use",
        "trademark-use",
    ],
    ("require", "demand", "require", "demand"): [
        "include-copyright",
        "disclose-source",
        "document-changes",
        "network-use-diclose",
        "same-license",
    ],
    ("offer", "give", "offer", "give"): ["liability", "warranty"],
}
intent_suggest_text = [
    "Tell me some licenses that",
    "Suggest me some licenses that",
    "Can you suggest me some licenses which",
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


def writeSuggestionInstances():
    with open("suggestions.txt", "w") as file:
        for i in range(10):
            sentence = ""
            sentence += random.choice(intent_suggest_text)
            cnt = 0
            word = None
            for key, value in key_permissions.items():
                if cnt == 0:
                    word = "allowed"
                elif cnt == 1:
                    word = "restricted"
                elif cnt == 2:
                    word = "offered"
                random_key = random.choice(key)
                random_permission_selections = random.randint(1, len(value))
                random_permissions = random.sample(value, random_permission_selections)
                sentence += f'"[{random_key}]({word}_word)" "['
                for permission in random_permissions:
                    sentence += f"{permission} ,"
                sentence = sentence[:-2]
                sentence += f'] ({word}_permissions)" '
                cnt += 1
            file.write("- " + sentence + "\n")


def writeSuggestionInstances2():
    with open("suggestions.txt", "w") as file:
        for i in range(200):
            sentence = ""
            sentence += random.choice(intent_suggest_text)
            cnt = 0
            word = None
            for key, value in key_permissions.items():
                if cnt == 0:
                    word = "allowed"
                elif cnt == 1:
                    word = "restricted"
                elif cnt == 2:
                    word = "offered"
                random_key = random.choice(key)
                random_permission_selections = random.randint(1, len(value))
                random_permissions = random.sample(value, random_permission_selections)
                sentence += (
                    f' "[{random.choice(negative_positive)+random_key}]({word}_word)" '
                )
                for permission in random_permissions:
                    sentence += f'"[{permission}]({word}_permissions)",'
                sentence = sentence[:-1]
                cnt += 1
            file.write("- " + sentence + "\n")


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
    licenses, ids = read_licenses_info("../newJSON/")
    with open("licenses.txt", "w") as file:
        for license in licenses:
            file.write(
                "- "
                + random.choice(intent_text)
                + '"['
                + license
                + '](license_name)" \n'
            )


# writeLicensesNames()
# writeLicensesIds()
writeLicensesIds()
