from typing import Any, Text, Dict, List
import os
import json
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from difflib import SequenceMatcher

titles = []
ids = []
descriptions = []
permissions = []
conditions = []
limitations = []
all_permissions = []
licenses_text = []
confirmed_license = None
choice_synonyms = {
    "allow": ["allow", "permit", "accept", "let", "grant", "authorize"],
    "deny": [
        "deny",
        "disallow",
        "ban",
        "block",
        "forbid",
        "prohibid",
    ],
    "require": ["require", "need", "demand", "insist"],
    "negative": [
        "do not",
        "don't",
        "does not",
        "doesn't",
        "is not",
        "isn't",
        "are not",
        "aren't",
        "dont",
        "doesnt",
        "not",
    ],
    "positive": ["do", "does", "is", "are"],
    "offer": ["offer", "give", "provide", "supply", "afford"],
}
word_values = {
    "allow": 1,
    "deny": 0,
    "negative": 0,
    "positive": 1,
    "offer": 1,
    "require": 1,
}
permission_synonyms = {
    "private-use": ["private use", "personally", "in private", "privately"],
    "commercial-use": [
        "commercial-use",
        "commercially",
        "profit",
        "make money",
        "sell",
    ],
    "modifications": ["modifications", "modify", "alter", "change", "edit"],
    "distribution": ["distribution", "share", "distribute", "send"],
    "sublicense": [
        "sublicense",
        "sublicensing",
        "create sublicense",
        "granting further licenses",
    ],
    "patent-use": [
        "patent-use",
        "patented products",
        "patent infringement",
        "patent claims",
    ],
    "include-copyright": [
        "include-copyright",
        "copyright notice",
        "mention the author",
        "copyright",
    ],
    "disclose-source": ["open-source", "share the source code", "disclose source"],
    "document-changes": [
        "mention modifications",
        "mention changes",
        "state changes",
        "state modifications",
        "write changes",
        "write modifications",
        "document changes",
        "document modifications",
    ],
    "network-use-disclose": [
        "using the software over a network",
        "disclosing network usage",
        "share modifications on a network",
    ],
    "warranty": ["warranty"],
}


def exist_similar(word, list, max_init):
    max_similarity_percentage = max_init
    for synonym in list:
        similarity = SequenceMatcher(None, word, synonym).ratio()
        if similarity > max_similarity_percentage:
            return 1

    return 0


def find_similar(input, dictionary):
    max_similarity_percentage = 0.0
    max_similarity_name = None

    for key, values in dictionary.items():
        for synonym in values:
            similarity = SequenceMatcher(None, input, synonym).ratio()

            if similarity > max_similarity_percentage:
                max_similarity_percentage = similarity
                max_similarity_name = key

    return max_similarity_name, max_similarity_percentage


def search_permissions(word, permissions, license_ids):
    value = None
    phrase = ""

    if len(word) > 1:
        word[0] += " " + word[len(word) - 1]

    subwords = word[0].split(" ")
    if len(subwords) > 2:
        if "not" or "nt" or "n't" in subwords:
            value = word_values["negative"]
        else:
            value = word_values["positive"]

        choice, percentage = find_similar(subwords[len(subwords) - 1], choice_synonyms)
        value = int(not (value ^ word_values[choice]))
    elif len(subwords) == 2:
        sign, percentage = find_similar(subwords[0], choice_synonyms)

        if percentage > 0.85:
            value = word_values[sign]

        choice, percentage = find_similar(subwords[1], choice_synonyms)
        value = int(not (value ^ word_values[choice]))
    else:
        value = 1
        choice, percentage = find_similar(subwords[0], choice_synonyms)
        value = int(not (value ^ word_values[choice]))

    if value == 1:
        print("Positive")
    else:
        print("Negative")

    if choice is "offer":
        value = ~value

    for permission in permissions:
        permission_list = permission.split(",")
        permissions.remove(permission)
        for permission_seperated in permission_list:
            permissions.append(permission_seperated)

    permissions = list(set(permissions))

    new_permissions = [
        check_permission_similarity(permission)[0] for permission in permissions
    ]
    suggested_licenses = [id for id in license_ids]
    print("New permissions: ", new_permissions)
    for permission in new_permissions:
        valid_licenses = []
        for i in range(len(suggested_licenses)):
            if value == 0:
                if permission not in all_permissions[ids.index(suggested_licenses[i])]:
                    valid_licenses.append(suggested_licenses[i])
            else:
                if permission in all_permissions[ids.index(suggested_licenses[i])]:
                    valid_licenses.append(suggested_licenses[i])

        new_suggested_licenses = [
            license for license in valid_licenses if license in suggested_licenses
        ]

    return new_suggested_licenses


def check_permission_similarity(input):
    max_similarity_percentage = 0.0
    max_similarity_name = None

    for permission, similar_permissions in permission_synonyms.items():
        for similar_permission in similar_permissions:
            similarity = SequenceMatcher(None, input, similar_permission).ratio()

            if similarity > max_similarity_percentage:
                max_similarity_percentage = similarity
                max_similarity_name = permission

    return max_similarity_name, max_similarity_percentage


def check_choice_similarity(input):
    return None


def list_files_in_directory(directory):
    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)

    return files


def read_licenses_info(folder_path):
    titles.clear()
    ids.clear()
    descriptions.clear()
    permissions.clear()
    conditions.clear()
    limitations.clear()
    all_permissions.clear()
    licenses_text.clear()

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
        licenses_text.append(data["license-text"])
        all_permissions.append(
            data["permissions"] + data["conditions"] + data["limitations"]
        )


def check_collision(choice):
    words = choice.split()
    max_similarity_percentage = 0.0
    permission = None
    for word in words:
        similarity_name, similarity_percentage = check_permission_similarity(word)
        if similarity_percentage > max_similarity_percentage:
            permission = similarity_name
            max_similarity_percentage = similarity_percentage

    return permission


def check_license_similarity(input, license_names, license_ids):
    max_name_similarity = 0.0
    max_id_similarity = 0.0
    max_name = None
    max_id = None

    # input = input.lower().replace(" ", "")

    for name in license_names:
        similarity = SequenceMatcher(None, input, name).ratio()
        # print("Name: ", name)
        # print("Similarity: ", similarity)
        if similarity > max_name_similarity:
            max_name_similarity = similarity
            max_name = name

    for id in license_ids:
        similarity = SequenceMatcher(None, input, id).ratio()
        if similarity > max_id_similarity:
            max_id_similarity = similarity
            max_id = id

    if max_name_similarity > max_id_similarity:
        max_id = license_ids[license_names.index(max_name)]
        return max_name, max_id, max_name_similarity
    max_name = license_names[license_ids.index(max_id)]
    return max_name, max_id, max_id_similarity


def check_license_permisssion(license_id, permission):
    index = ids.index(license_id)
    if permission in all_permissions[index]:
        return 1
    return 0


class GetLicenseInfo(Action):

    def name(self) -> Text:
        return "action_get_license"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        read_licenses_info("./licensesJSON/")
        license_parameter = tracker.get_slot("license_name")
        license_name, license_id, max_similarity = check_license_similarity(
            license_parameter, titles, ids
        )
        print("License name:", license_name)
        # Do something with the parameters
        dispatcher.utter_message(
            text=f"Do you mean the following software license: {license_name} ({license_id}) ."
        )
        tracker.slots["confirmed_license_name"] = license_name
        return [events.SlotSet("confirmed_license_name", license_name)]


class LicenseInfoProvider(Action):

    def name(self) -> Text:
        return "action_get_license_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # license_name = tracker.get_slot("license_name")
        # Do something with the parameters
        print("Confirmed License: ", tracker.get_slot("confirmed_license_name"))
        index = titles.index(tracker.get_slot("confirmed_license_name"))
        license_text = ""
        for line in licenses_text[index]:
            license_text += line + "\n"
        dispatcher.utter_message(
            text=f"Here is the License full text: \n {license_text}"
        )

        return []


class LicensePermissionInfo(Action):

    def name(self) -> Text:
        return "action_check_permission"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # license_name = tracker.get_slot("license_name")
        # Do something with the parameters
        read_licenses_info("./licensesJSON/")
        permission = tracker.get_slot("permission")
        choice = tracker.get_slot("choice")
        license_name = tracker.get_slot("license_name")
        print("Pemission: ", permission)
        print("Choice: ", choice)
        print("License: ", license_name)
        license_name, license_id, license_similarity = check_license_similarity(
            license_name, titles, ids
        )

        if permission is None:
            permission = check_collision(choice)
            print("After collision check pemission: ", permission)
        else:
            permission, permission_similarity_percentage = check_permission_similarity(
                permission
            )

        if check_license_permisssion(license_id, permission):
            dispatcher.utter_message(
                text=f"License name: {license_name} allows {permission}"
            )
        else:
            dispatcher.utter_message(
                text=f"License name: {license_name} doesn't allow {permission}"
            )

        return []


class LicenseSuggestion(Action):

    def name(self) -> Text:
        return "action_suggest_license"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        allowed_permissions = tracker.get_slot("allowed_permissions")
        restricted_permissions = tracker.get_slot("restricted_permissions")
        offered_permissions = tracker.get_slot("offered_permissions")
        allowed_word = tracker.get_slot("allowed_word")
        restricted_word = tracker.get_slot("restricted_word")
        offered_word = tracker.get_slot("offered_word")
        read_licenses_info("./licensesJSON/")
        message = f"Allowed permissions: {allowed_permissions} , restricted permissions: {restricted_permissions} , offered permissions: {offered_permissions} , allowed word: {allowed_word} , restricted word: {restricted_word} , offered word: {offered_word}"
        dispatcher.utter_message(text=message)
        print(f"Allowed permissions: {allowed_permissions} ")
        suggested_licenses = search_permissions(allowed_word, allowed_permissions, ids)
        print(suggested_licenses)
        suggested_licenses = search_permissions(
            restricted_word, restricted_permissions, suggested_licenses
        )
        print(suggested_licenses)
        suggested_licenses = search_permissions(
            offered_word, offered_permissions, suggested_licenses
        )
        print(suggested_licenses)

        # for permission in allowed_permissions:
        #     print(permission)

        return [AllSlotsReset()]
