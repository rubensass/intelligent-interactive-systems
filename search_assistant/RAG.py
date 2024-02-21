import os
from dotenv import load_dotenv

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader

load_dotenv("local.env")


class RAG:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.documents_path = "../all_books"
        self.embedding = OpenAIEmbeddings()
        self.persist_directory = "db"

    def download_documents(self):
        loader = DirectoryLoader(
            self.documents_path, glob="./*.txt", loader_cls=TextLoader
        )
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        return texts

    def get_vector_db(self):
        if not os.path.exists(self.persist_directory):
            texts = self.download_documents()
            vectordb = Chroma.from_documents(
                documents=texts,
                embedding=self.embedding,
                persist_directory=self.persist_directory,
            )
            vectordb.persist()
            vectordb = None
        vectordb = Chroma(
            persist_directory=self.persist_directory, embedding_function=self.embedding
        )
        return vectordb

    def get_qa_chain(self):
        vectordb = self.get_vector_db()
        retriever = vectordb.as_retriever(search_kwargs={"k": 10})
        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        return qa_chain


# if __name__ == "__main__":
#     rag = RAG()
#     print("HEY")
