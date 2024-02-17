from typing import Any, Text, Dict, List
import os
import json
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
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
}


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
            permission = check_permission_similarity(permission)

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
        dispatcher.utter_message(text=f"License names: {allowed_permissions}")

        return []
