from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ProcessParameters(Action):

    def name(self) -> Text:
        return "action_license_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        license = tracker.get_slot("license_name")

        # Do something with the parameters
        dispatcher.utter_message(text=f"You provided License name: {license} .")

        return []
