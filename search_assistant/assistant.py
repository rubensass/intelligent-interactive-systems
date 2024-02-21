from search_assistant.RAG import RAG


def process_llm_response(llm_response):
    answer = llm_response["result"]
    answer += "\n\nSources:"
    for source in llm_response["source_documents"]:
        answer += "\n" + source.metadata["source"]
    return answer


class Assistant:
    def __init__(self):
        self.chat_memory = None
        self.memory_prompt = f"""If you need the previous conversations
        with the client to answer a query, you must use exclusivaly in CHAT_MEMORY:
        {self.chat_memory}
        """
        self.system_prompt = """
        <SYSTEM> 
        You are a helpful shopping assistant working in a book store, your task is to
        assist the client during his entire shopping process so he will find a book to buy.
        Answer the client's query politely with a friendly tone. 
        """
        self.qa_chain = RAG().get_qa_chain()

    def ask_to_assistant(self, query: str):
        if query == "stop":
            answer = "Goodbye, have a nice day!"
            self.chat_memory = None
        else:
            if self.chat_memory:
                self.system_prompt = (
                    f"""{self.system_prompt} {self.memory_prompt} </SYSTEM>"""
                )
            else:
                self.system_prompt = f"""{self.system_prompt} </SYSTEM>"""
            full_query = f"""{self.system_prompt} <USER_QUERY>{query}</USER_QUERY>"""
            llm_response = self.qa_chain(full_query)
            answer = process_llm_response(llm_response)
            self.memory += f"""USER: {query}
            YOUR_ANSWER: {answer}"""
        return answer
