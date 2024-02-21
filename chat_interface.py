from search_assistant.assistant import Assistant

answer = ""
assistant = Assistant()

# TO STOP THE CONVERSATION TELL 'stop' TO THE ASSISTANT #

print("Assistant: Hello, welcome to our store, how may I help you?")
print(" ")

while answer != "Goodbye, have a nice day!":
    query = input()
    # print("Me: " + query)
    print(" ")
    answer = assistant.ask_to_assistant(query)
    print(answer)
    print(" ")
