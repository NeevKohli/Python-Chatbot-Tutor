import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title
import time

with st.spinner('Loading ...'):
    time.sleep(3)

st.title("Important Information :octagonal_sign:")
st.markdown("""
    Disclaimer: User feedback is extremely valuable to us as developers.
    When interacting with PyBot, you will be prompted to provide optional feedback after every response. 
    If you choose to submit feedback then this will be anonymously recorded and analysed for research purposes. 

    Terms of Service (ToS): PyBot will only be used in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). 
    OpenAIs usage policies (https://openai.com/policies/usage-policies) will be abided by at all times whilst using PyBot.
    """)

#check if username is text before proceeding (it cannot be alphanumeric)

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page(r"pages/Welcome.py", "Home", ":house:"),
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:"),
        Page(r"pages/PyBot.py", "PyBot", ":snake:")
    ]
)

hide_pages(
    [
        Page(r"pages/Login.py", "Login", ":key:"),
    ]    
)

Home = st.button("Home :house:")
if Home:
    switch_page("Home")

Chatbot = st.button("PyBot :snake:")
if Chatbot:
    switch_page("PyBot")