import streamlit as st


def main():
    st.set_page_config(page_title="Chat with your shopping assistant")
    st.header("Chat with your shopping assistant")
    st.text_input("How can I help you today?")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv("local.env")
    print(os.getenv("OPENAI_API_KEY"))
