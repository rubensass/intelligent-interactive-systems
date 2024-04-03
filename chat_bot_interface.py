import streamlit as st
from streamlit_chat import message
from search_assistant.assistant import Assistant
import time

st.set_page_config(page_title="Welcome to your shopping assistance service", page_icon="🛒", layout="wide", 
                    menu_items={'Get Help': 'mailto:max.bershtman@gmail.com','Report a bug': "mailto:max.bershtman@gmail.com", 'About': "Your Personal Shopping Assistant Made with ❤️ by Max and Ruben"})
                    
#✨

my_expander = st.expander("**If You Want To Create A Profile - Press Here**", expanded=False)
with my_expander:
    st.write("To create a profile, just copy the following form and fill it up with your personal information and then send it in the chat:")
    st.write("{'name': 'write here your name', 'age': 'write here your age', 'gender': 'write here your gender', 'hobbies': 'write here your hobbies'}")
    st.write("**Please make sure to write the information exectly as it is written in the form but everywhere where you see 1 quate - ' put double quotes instead - '' **")
    st.write("For example you can write this in the chat: {''name'': ''Max'', ''age'': ''10'' , ''gender'': ''Male'', ''hobbies'': ''swimming''}")
    st.write("**Your profile will be saved and you will be able to connect to it whenever you want - after connecting the chat will remember your information.**")

my_expander2 = st.expander("**If You Want To Log Into Your Profile - Press Here**", expanded=False)
with my_expander2:
    st.write("To log into your profile, just copy the following form and fill it up with your personal information and then send it in the chat:")
    st.write("{'name': 'write here your name'}")
    st.write("**Please make sure to write the information exectly as it is written in the form but everywhere where you see 1 quate - ' put double quotes instead - '' **")
    st.write("For example you can write this in the chat: {''name'': ''Max''}")
    st.write("**After logging in, the chat will remember your information and adapt the service to your personal profile.**")


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


my_expander3 = st.expander("**Press Here To See Some Ideas Of What You Can Ask**", expanded=False)
with my_expander3:
    st.write("Provide me a book suggestion for a 10 year boy") 
    st.write("Give me the best book about vempires you have in the store")
    st.write("give me a long book that costs less than 20$")
    

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

