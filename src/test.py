# from difflib import SequenceMatcher

# print(SequenceMatcher(None, "aren t", "arent").ratio())
# message = "modifications,document-changes"
# message2 = "sssssssss"

# print(message.split(","))
# print(message2.split(","))
my_list = ["apple", "banana", "cherry", "apple", "mango", "orange", "cherry"]
unique_list = list(set(my_list))

print(f"Original list: {my_list}")
print(f"List with duplicates removed: {unique_list}")
