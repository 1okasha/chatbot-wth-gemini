import os
import streamlit as st
import google.generativeai as gen_ai
from dotenv import load_dotenv

load_dotenv()  #pass key from env to the envirnment variable

#pg configuration on streamlit
st.set_page_config(
    page_title="chatbot with gemini",
    layout="centered",
)
#calling api key from env
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=GOOGLE_API_KEY)
model=gen_ai.GenerativeModel("gemini-pro")

def translate_role_for_streamlit(user_role):
    if user_role=="model":
        return "assistant"
    else:return user_role

#to maintained history(when new query is asked we donot lose the previous query)
if "chat_session" not in st.session_state:
    st.session_state.chat_session=model.start_chat(history=[])

st.title("GEMINI-PRO CHATBOT")

#to display HISTORY SHOW
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# input field for user msg
user_prompt=st.chat_input("ask something")
if user_prompt:
    #display prompt that is entered by the user
    st.chat_message("user").markdown(user_prompt)

    #send user msg to gemini to find response
    gemini_response=st.session_state.chat_session.send_message(user_prompt)

    # desplay the output
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

