from typing import Any, Text, Dict, List
import os
import json
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import FollowupAction
from difflib import SequenceMatcher


class License:
    def __init__(self):
        self.title = None
        self.id = None
        self.description = None
        self.permissions = {
            "commercial-use": 0,
            "distribution": 0,
            "modifications": 0,
            "private-use": 0,
            "patent-use": 0,
            "sublicense": 0,
        }
        self.conditions = {
            "include-copyright": 0,
            "document-changes": 0,
            "disclose-source": 0,
            "network-use-disclose": 0,
            "same-license": 0,
        }
        self.limitations = {"liability": 0, "warranty": 0, "trademark-use": 0}

    def set_info(self, conditions, limitations, permissions, title, description, id):
        for cond in conditions:
            self.conditions[cond] = 1
        for perm in permissions:
            self.permissions[perm] = 1
        for lim in limitations:
            self.limitations[lim] = 1
        self.all_rights = self.conditions.copy()
        self.all_rights.update(self.permissions)
        self.all_rights.update(self.limitations)

        self.id = id
        self.title = title
        self.description = description

    def print_info(self):
        print(self.permissions)
        print(self.limitations)
        print(self.conditions)
        print(self.id)
        print(self.title)
        print(self.description)


titles = []
ids = []
licenses = []
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
key_permissions = {
    "allow": [
        "commercial-use",
        "modifications",
        "distribution",
        "private-use",
        "sublicensing",
        "patent-use",
        "trademark-use",
    ],
    "require": [
        "include-copyright",
        "disclose-source",
        "document-changes",
        "network-use-diclose",
        "same-license",
    ],
    "offer": ["liability", "warranty"],
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
    "same-license": ["same-license", "identical-license", "includes-license"],
    "warranty": ["warranty"],
    "liability": ["liability"],
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

    if choice is "offer":
        value = ~value

    for permission in permissions:
        permission_list = permission.split(",")
        permissions.remove(permission)
        for permission_seperated in permission_list:
            permissions.append(permission_seperated)

    permissions = list(set(permissions))

    correct_permissions = [
        check_permission_similarity(permission)[0] for permission in permissions
    ]
    if value == 1:
        print("Positive")
        phrase += f" {choice} "
    else:
        print("Negative")
        phrase += f" don't {choice}"
    suggested_licenses = [id for id in license_ids]
    for permission in correct_permissions:
        phrase += f" {permission} ,"
        valid_licenses = []
        for i in range(len(suggested_licenses)):
            if value == 0:
                if permission not in all_permissions[ids.index(suggested_licenses[i])]:
                    valid_licenses.append(suggested_licenses[i])
            else:
                if permission in all_permissions[ids.index(suggested_licenses[i])]:
                    valid_licenses.append(suggested_licenses[i])

        suggested_licenses = [
            license for license in valid_licenses if license in suggested_licenses
        ]

    return suggested_licenses, phrase[:-1]


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
    licenses.clear()

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
        license = License()
        license.set_info(
            data["conditions"],
            data["limitations"],
            data["permissions"],
            data["title"],
            data["description"],
            data["spdx-id"],
        )
        licenses.append(license)


def getLicenseInfo(license_ids):
    license_permissions = []
    license_titles = []
    print(license_ids)
    for id in license_ids:
        for license in licenses:
            if id == license.id:
                license_permissions.append(
                    [license.permissions, license.conditions, license.limitations]
                )
                license_titles.append(license.title)

    return license_permissions, license_titles


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
        if permission == "warranty" or permission == "liability":
            return 0
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
            text=f"Do you mean the following software license: {license_name} ({license_id}) .",
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
        read_licenses_info("./licensesJSON/")
        print("Confirmed License: ", tracker.get_slot("confirmed_license_name"))
        index = titles.index(tracker.get_slot("confirmed_license_name"))
        license_id = [licenses[index].id]
        license_permissions, license_titles = getLicenseInfo(license_id)
        print("License id: ", license_id)
        json_mess = {
            "key": "license_info",
            "license_id": license_id,
            "license_titles": license_titles,
            "license_permissions": license_permissions,
        }
        dispatcher.utter_message(
            text=f"{licenses[index].id} ({licenses[index].title}) : \n {licenses[index].description}",
            json_message=json_mess,
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

        choice, similarity = find_similar(permission, key_permissions)
        if check_license_permisssion(license_id, permission):
            dispatcher.utter_message(
                text=f"License name: {license_name} {choice} {permission}"
            )
        else:
            dispatcher.utter_message(
                text=f"License name: {license_name} doesn't {choice} {permission}"
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
        print(message)
        license_ids = [license_id for license_id in ids]
        output_message = f"Here are some licenses that"

        if allowed_word is not None:
            license_ids, allowed_phrase = search_permissions(
                allowed_word, allowed_permissions, ids
            )
            output_message += f" {allowed_phrase}"

        if restricted_word is not None:
            license_ids, restricted_phrase = search_permissions(
                restricted_word, restricted_permissions, license_ids
            )
            output_message += f" and {restricted_phrase}"

        if offered_word is not None:
            license_ids, offered_phrase = search_permissions(
                offered_word, offered_permissions, license_ids
            )
            output_message += f" and {offered_phrase}"

        output_message += " : \n"
        # output_message = f"Here are some licenses that{allowed_phrase } and{restricted_phrase} and{offered_phrase} : \n"
        licenses_full_name = []
        for license_id in license_ids:
            index = ids.index(license_id)
            licenses_full_name.append(titles[index])

        for i in range(len(license_ids)):
            output_message += f" {licenses_full_name[i]} ({license_ids[i]}) ,"
        output_message = output_message[:-1]

        license_permissions, license_titles = getLicenseInfo(license_ids)

        json_mess = {
            "key": "permission_suggested_licenses",
            "license_ids": license_ids,
            "license_titles": licenses_full_name,
            "license_permissions": license_permissions,
        }
        if(allowed_word is None and  restricted_word is None and offered_word is None) :
            output_message="I am afraid you didn't finish your question. In more details you can find all the licenses i can suggest!"
        dispatcher.utter_message(text=output_message, json_message=json_mess)

        return [AllSlotsReset()]


class start_Tutorial(Action):
    def name(self) -> Text:
        return "action_start_tutorial"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        output_message = "Let me guide you find the appropriate license through a series of questions. Can you please choose your knowledge on Software Licenses?"
        json_mess = {
            "key": "start-tutorial",
        }
        dispatcher.utter_message(text=output_message, json_message=json_mess)

        return []


# class AskQuestion(Action):
#     def name(self) -> Text:
#         return "action_ask_question"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         answer = tracker.latest_message["text"]
#         dispatcher.utter_message(text="Question")
#         if "Stop" in answer or "stop" in answer:
#             dispatcher.utter_message(text="Finished")

#         return []
