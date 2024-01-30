import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages,  add_page_title
import streamlit_authenticator as stauth

#Login page - user enters credentials (username and/or password) to access conversation history (archived from previous sessions)
#Hash (encrypt) them for user privacy and security before implementing end-user IDs for OpenAI to monitor via the moderation endpoint tool
#better than Session IDs which are only valid for a single session so users cannot access their conversation history

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

flag=False

# Insert a form in the container
with placeholder.form(key="login"):
    while flag==False:
        st.markdown("#### Enter your credentials")
        email = st.text_input("Email", key="emaila")
        password = st.text_input("Password", key="passworda", type="password")
        submit = st.form_submit_button("Login")

        if submit and email == actual_email and password == actual_password:
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            placeholder.empty()
            st.success("Login successful")
            flag=True

        elif submit and email != actual_email and password != actual_password:
            st.error("Login failed")

#check if username is text before proceeding (it cannot be alphanumeric)
if flag==True:
    show_pages(
        [
            Page("Home.py", "Home", ":house:"),
            Page("Info.py", "Important Information", ":octagonal_sign:")
        ]
    )

    hide_pages(
        [
            Page("Chatbot.py", "PyBot", ":snake:")
        ]
    )

    switch_page("Home")