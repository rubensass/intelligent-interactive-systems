from search_assistant.RAG import RAG
from openai import OpenAI
import os
import json


from dotenv import load_dotenv

load_dotenv("local.env")


def process_llm_response(llm_response):
    answer = llm_response["result"]
    return answer


def is_create_profile(query):
    answer = False
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system_prompt = f"""You are an intent classifier. I'll provide you with text and I will ask about the intent of the text 
    and you'll answer by YES or NO. Your answer should be brief. 
    """
    task = f"A person sent you the following query: '{query}'. Does the person want to create a Profile?"
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": task},
        ],
    )
    response = response.choices[0].message.content
    if response:
        if response == "YES":
            answer = True
    return answer


def is_profile_creation_answer(query):
    answer = False
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    task = f"A person sent you the following query: '{query}'. Does the query has the following format: "
    task += "{'name': a name, 'age': an age, 'gender': a gender, 'hobbies': hobbies}?"
    task += "you must answer briefly by YES or NO."

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": " ",
            },
            {"role": "user", "content": task},
        ],
    )
    response = response.choices[0].message.content
    if response:
        if response == "YES":
            answer = True
    return answer


def is_login_profile(query):
    answer = False
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system_prompt = f"""You are an intent classifier. I'll provide you with text and I will ask about the intent of the text 
    and you'll answer by YES or NO. Your answer should be brief. 
    """
    task = f"A person sent you the following query: '{query}'. Does the person want to log into his/her Profile?"
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": task},
        ],
    )
    response = response.choices[0].message.content
    if response:
        if response == "YES":
            answer = True
    return answer


def is_login_profile_answer(query):
    answer = False
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    task = f"A person sent you the following query: '{query}'. Does the query has the following format: "
    task += "{'name': a name}?"
    task += "you must answer briefly by YES or NO."

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": " ",
            },
            {"role": "user", "content": task},
        ],
    )
    response = response.choices[0].message.content
    if response:
        if response == "YES":
            answer = True
    return answer


class Assistant:
    def __init__(self):
        self.system_prompt = """
<SYSTEM> 
You are a helpful shopping assistant working in a book store, your task is to
assist the client during his entire shopping process so he will find a book to buy. Your are only allowed to advice about books for which you have access to its purchasing
url and its retail price.
Answer the client's query politely with a friendly tone. Your answer should not be too long and respond exclusively to the users query
except if the user is asking for details. Do not push the user too much to buy a product. 
</SYSTEM>
"""
        self.qa_chain = RAG().get_qa_chain()
        self.create_profile_answer = """Hey, I am happy to see that you want to create your own profile! To do so, copy the following form:
{"name": "enter your name", "age": "enter your age", "gender": "enter your gender", "hobbies": "enter your hobbies"}, fill it up and send it back
in the chat."""
        self.create_profile_confirmation = """Your profile have been created, you can tell your assistant to connect to your profile whenever you want."""
        self.login_profile_answer = """Hey, I noticed that you wanted to log into your profile. To do so, copy the following form:
{"name": "enter your name"}, fill it up and send it back in the chat."""
        self.login_profile_confirmation = """You logged into your profile with success! From now on, any interaction with you assistant will take into account 
your personal information."""

    def ask_to_assistant(self, query):
        profile_creation = is_profile_creation_answer(query["text"])
        if profile_creation:
            profile_json = json.loads(query["text"])
            name = profile_json["name"].replace(" ", "_")
            json_string = json.dumps(profile_json)
            with open(f"user_profiles/{name}.json", "w") as json_file:
                json_file.write(json_string)
            answer = self.create_profile_confirmation
            return answer

        logged_into_profile = is_login_profile_answer(query["text"])
        if logged_into_profile:
            profile_json = json.loads(query["text"])
            name = profile_json["name"]
            with open(f"user_profiles/{name}.json", "r") as json_file:
                json_string = json_file.read()
            answer = self.login_profile_confirmation
            self.system_prompt = self.system_prompt.replace("</SYSTEM>", "")
            self.system_prompt += f"""You must adapt your service/advices/answers to the profile of the user. 
            The profile of the user is the following: {json_string}"""
            self.system_prompt += "</SYSTEM>"
            return answer

        create_profile = is_create_profile(query["text"])
        if create_profile:
            answer = self.create_profile_answer
            return answer

        login_profile = is_login_profile(query["text"])
        if login_profile:
            answer = self.login_profile_answer
            return answer

        query["text"] = f"""{self.system_prompt}\nUSER_QUERY:\n{query["text"]}"""
        query = str(query)
        llm_response = self.qa_chain(query)
        answer = process_llm_response(llm_response)
        return answer


# if __name__ == "__main__":
#     assistant = Assistant()

#     query2 = {"text": "I would like to create a profile"}
#     query3 = {
#         "text": '{"name": "Ruben", "age": "10", "gender": "male", "hobbies": "Vampires"}'
#     }
#     query4 = {"text": "I want to log into my profile"}
#     query5 = {"text": '{"name": "Ruben"}'}

#     answer2 = assistant.ask_to_assistant(query2)
#     answer3 = assistant.ask_to_assistant(query3)
#     answer4 = assistant.ask_to_assistant(query4)
#     answer5 = assistant.ask_to_assistant(query5)

#     print("HEYY")
