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
intent_of_specific_permission = [
    "Does the [license_name] [choice] [permission] ?",
    "The [license_name] [choice] [permission] ?",
    "[license_name] [choice] [permission] ?",
    "[choice] [permission] [license_name] ",
]
key_permissions = {
    ("permit", "allow", "accept", "forbid", "deny"): [
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
    ("offer", "give", "offer", "provide", "provide"): ["liability", "warranty"],
}
permissions = [
    "commercial-use",
    "modifications",
    "distribution",
    "private-use",
    "sublicensing",
    "patent-use",
    "trademark-use",
    "include-copyright",
    "disclose-source",
    "document-changes",
    "network-use-diclose",
    "same-license",
    "liability",
    "warranty",
]
choices = [
    "permit",
    "allow",
    "accept",
    "forbid",
    "deny",
    "require",
    "demand",
    "give",
    "offer",
    "provide",
]

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


def writeSuggestionInstances3():
    choice_keys = list(key_permissions.keys())

    with open("suggestions.txt", "w") as file:
        for i in range(100):
            permission_list = [permission for permission in permissions]
            sentence = ""
            sentence += random.choice(intent_suggest_text)
            cnt = 0
            word = None

            subset_length = random.randint(1, 5)

            # Pick a random subset
            random_subset = random.sample(permission_list, subset_length)

            # Remove the elements of the random subset from the original list
            permission_list = [
                element for element in permission_list if element not in random_subset
            ]

            random_key = random.choice(choice_keys[0])
            sentence += (
                f' "[{random.choice(negative_positive)+random_key}](allowed_word)" '
            )
            for permission in random_subset:
                sentence += f'"[{permission}](allowed_permissions)",'
            sentence = sentence[:-1] + " and "

            subset_length = random.randint(1, 3)

            # Pick a random subset
            random_subset = random.sample(permission_list, subset_length)

            # Remove the elements of the random subset from the original list
            permission_list = [
                element for element in permission_list if element not in random_subset
            ]

            random_key = random.choice(choice_keys[1])
            sentence += (
                f' "[{random.choice(negative_positive)+random_key}](restricted_word)" '
            )
            for permission in random_subset:
                sentence += f'"[{permission}](restricted_permissions)",'
            sentence = sentence[:-1] + " and "

            subset_length = random.randint(1, 2)

            # Pick a random subset
            random_subset = random.sample(permission_list, subset_length)

            # Remove the elements of the random subset from the original list
            permission_list = [
                element for element in permission_list if element not in random_subset
            ]

            random_key = random.choice(choice_keys[2])
            sentence += (
                f' "[{random.choice(negative_positive)+random_key}](offered_word)" '
            )
            for permission in random_subset:
                sentence += f'"[{permission}](offered_permissions)",'

            sentence = sentence[:-1] + " and "

            cnt += 1
            file.write("- " + sentence + "\n")


def writeSuggestionInstances4():
    choice_keys = list(key_permissions.keys())

    with open("suggestions.txt", "w") as file:
        for i in range(100):
            permission_list = [permission for permission in permissions]
            sentence = ""
            sentence += random.choice(intent_suggest_text)
            cnt = 0
            word = None

            subset_length = random.randint(1, 5)

            # Pick a random subset
            random_subset = random.sample(permission_list, subset_length)

            # Remove the elements of the random subset from the original list
            permission_list = [
                element for element in permission_list if element not in random_subset
            ]

            random_key = random.choice(choice_keys[0])
            sentence += (
                f' "[{random.choice(negative_positive)+random_key}](allowed_word)" '
            )
            for permission in random_subset:
                sentence += f'"[{permission}](allowed_permissions)",'
            sentence = sentence[:-1] + " and "

            subset_length = random.randint(1, 3)

            # Pick a random subset
            random_subset = random.sample(permission_list, subset_length)

            # Remove the elements of the random subset from the original list
            permission_list = [
                element for element in permission_list if element not in random_subset
            ]

            random_key = random.choice(choice_keys[1])
            sentence += (
                f' "[{random.choice(negative_positive)+random_key}](restricted_word)" '
            )
            for permission in random_subset:
                sentence += f'"[{permission}](restricted_permissions)",'
            sentence = sentence[:-1] + " and "

            # subset_length = random.randint(1, 2)

            # # Pick a random subset
            # random_subset = random.sample(permission_list, subset_length)

            # # Remove the elements of the random subset from the original list
            # permission_list = [
            #     element for element in permission_list if element not in random_subset
            # ]

            # random_key = random.choice(choice_keys[2])
            # sentence += (
            #     f' "[{random.choice(negative_positive)+random_key}](offered_word)" '
            # )
            # for permission in random_subset:
            #     sentence += f'"[{permission}](offered_permissions)",'

            # sentence = sentence[:-1]

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


def writeSpecificPermissions(n):
    licenses, ids = read_licenses_info("../licensesJSON/")
    with open("suggestions.txt", "w") as file:
        for i in range(len(licenses)):
            line = "- " + random.choice(intent_of_specific_permission)
            line = line.replace(
                "[permission]", f'"[{random.choice(permissions)}](permission)"'
            )
            line = line.replace("[license_name]", f'"[{licenses[i]}](license_name)"')
            line = line.replace("[choice]", f'"[{random.choice(choices)}](choice)"')
            file.write(line + "\n")


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
# writeLicensesIds()
writeSuggestionInstances4()
