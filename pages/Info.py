import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title
import time

st.title("Important Information :octagonal_sign:")
st.markdown("""
    Terms of Service (ToS): PyBot will only be used in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). OpenAIs usage policies (https://openai.com/policies/usage-policies) will be abided by at all times whilst using PyBot.
    """)

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

#Home = st.button("Home :house:")
#if Home:
#    switch_page("Home")

#Chatbot = st.button("PyBot :snake:")
#if Chatbot:
#    switch_page("PyBot")