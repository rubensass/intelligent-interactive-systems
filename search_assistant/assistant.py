from search_assistant.RAG import RAG


def process_llm_response(llm_response):
    answer = llm_response["result"]
    return answer


class Assistant:
    def __init__(self):
        self.system_prompt = """
<SYSTEM> 
You are a helpful shopping assistant working in a book store, your task is to
assist the client during his entire shopping process so he will find a book to buy.
Answer the client's query politely with a friendly tone. Your answer should not be too long and respond exclusively to the users query
except if the user is asking for details. Do not push the user too much to buy a product.
</SYSTEM>
"""
        self.qa_chain = RAG().get_qa_chain()

    def ask_to_assistant(self, query):
        if len(query["past_user_inputs"]) <= 1:
            query["text"] = f"""{self.system_prompt}\nUSER_QUERY:\n{query["text"]}"""
        query = str(query)
        llm_response = self.qa_chain(query)
        answer = process_llm_response(llm_response)
        return answer
