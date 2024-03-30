import streamlit as st
from streamlit_chat import message
from search_assistant.assistant import Assistant
import time

st.set_page_config(page_title="Welcome to your shopping assistance service", page_icon="🛒", layout="wide", 
                    menu_items={'Get Help': 'mailto:max.bershtman@gmail.com','Report a bug': "mailto:max.bershtman@gmail.com", 'About': "Your Personal Shopping Assistant Made with ❤️ by Max and Ruben"})
                    
#✨
assistant = Assistant()
...     

# Manually create a "rainbow" effect for the word "FindFairy"
rainbow_title = """
<h1 style='text-align: center; font-size: 100px;'>  
    🧚‍♀️<span style='color: #FF0000;'>F</span>
    <span style='color: #FF7F00;'>i</span>
    <span style='color: #FFFF00;'>n</span>
    <span style='color: #00FF00;'>d</span>
    <span style='color: #0000FF;'>F</span>
    <span style='color: #4B0082;'>a</span>
    <span style='color: #9400D3;'>i</span>
    <span style='color: #FF0000;'>r</span>
    <span style='color: #FF7F00;'>y</span> 🧚‍♀️
</h1>
<h2 style='text-align: center; font-size: 24px; color: white;'>
    Your Personal Guide For A Magical Shopping Experience
</h2>
"""
st.markdown(rainbow_title, unsafe_allow_html=True)



if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def query(payload):
    return assistant.ask_to_assistant(payload)


def get_text():
    input_text = st.text_input("Ask me for help: ", value=None, placeholder = "Enter Your Question Here")
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
else:
    output = None

st.session_state.past.append(user_input)
st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

# Button to start over or finish
if st.button("Press Here To Start Over Or Finish"):
    # Reset session state
    st.session_state["generated"] = []
    st.session_state["past"] = []

    # Display a thank you message and balloons
    st.text("Thank you for using FindFairy!")
    st.balloons()
    time.sleep(1)

    # Rerun the app from the top
    st.experimental_rerun()

#streamlit run chat_bot_interface.py