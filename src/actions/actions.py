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
licenses_text = []
confirmed_license = None


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


def check_similarity(input, license_names, license_ids):
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
        license_name, license_id, max_similarity = check_similarity(
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
