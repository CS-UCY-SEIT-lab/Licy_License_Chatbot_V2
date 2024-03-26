import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore
from BasicTree import BasicTree
import jsonpickle


def delete_collection(coll_ref, batch_size):
    if batch_size == 0:
        return

    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
user_ref = db.collection("users")

delete_collection(user_ref, 5)

# initial_subset = ["ok", "ok"]
# tree = BasicTree(None, None, initial_subset)

# tree_json = jsonpickle.encode(tree)

# user_ref.add({"UserID": 1000, "Tree": tree_json})

# target_user_id = 1000  # Replace with the actual user ID

# user_ref = db.collection("users")
# # Query based on the user ID field
# query = user_ref.where("UserID", "==", target_user_id)  # "==" is equality comparison

# # Get all matching documents (should be at most 1 for unique user IDs)
# user_snapshot = query.get()

# if user_snapshot:
#     # Access the document data (assuming there's a match)
#     user_data = user_snapshot[0].to_dict()
#     user_snapshot[0].reference.update({"Tree": "pampos"})
#     print(user_data)
# else:
#     print("No user found with ID:", target_user_id)

# emp_ref = db.collection("users")
# docs = emp_ref.stream()

# for doc in docs:
#     print("{} => {} ".format(doc.id, doc.to_dict()))
