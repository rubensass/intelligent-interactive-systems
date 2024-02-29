import streamlit as st
from streamlit_chat import message
from search_assistant.assistant import Assistant

assistant = Assistant()

st.set_page_config(page_title="Welcome to your shopping assistance service")

st.header("Welcome to your shopping assistance service")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def query(payload):
    return assistant.ask_to_assistant(payload)


def get_text():
    input_text = st.text_input("You: ", "Start Shopping Assistant", key="input")
    return input_text


user_input = get_text()

if user_input:
    output = query(
        {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        }
    )

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
