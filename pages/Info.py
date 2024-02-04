import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title

st.title("Important Information :octagonal_sign:")
st.markdown("""
    Disclaimer: PyBot is GDPR compliant. All users will remain anonymous and all inputs provided to PyBot will not be used for further training. Please refer to Dr. Alejandra Beghelli for further information.

    Terms of Service (ToS): PyBot should only be used for summative assessments in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). PyBot does not condone, incite and/or generates inappropriate content that violates OpenAIs usage policies (https://openai.com/policies/usage-policies).
    By using this application, you acknowledge the Disclaimer and agree to abide by the ToS.
    """)

#check if username is text before proceeding (it cannot be alphanumeric)

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page(r"pages/Welcome.py", "Welcome", ":house:"),
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:"),
        Page(r"pages/PyBot.py", "PyBot", ":snake:")
    ]
)

hide_pages(
    [
        Page(r"pages/Login.py", "Login", ":key:"),
    ]    
)

Home = st.button("Welcome :house:")
if Home:
    switch_page("Welcome")

Chatbot = st.button("PyBot :snake:")
if Chatbot:
    switch_page("PyBot")