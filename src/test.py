from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


print(similar("Ioulianos", "Ioulianos"))

#  - story: user asks for license information
#     steps:
#       - intent: ask_for_license_info
#       - action:

#  - intent: ask_for_license_info
#     examples: |
#       - Can i have some information about [London](license_name)?
#       - Give me some info on [Paris](license_name)
#       - What do you know about [Rome](license_name)

#  - ask_for_license_info
