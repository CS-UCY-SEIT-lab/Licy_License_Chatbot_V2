import cohere

co = cohere.Client(
    api_key="cKPFgi2NQ2TqpBQstpGtzxkB5J42umudtRYxOhEB",
)

chat = co.chat(message="What is GPL2.0 license?", model="command")

print(chat.text)
