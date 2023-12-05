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
flag=False

while flag==False:
    # Insert a form in the container
    with st.form(key="login"):
        #Single
        st.title(":wave:")
        username = st.text_input("Username")
        submit = st.form_submit_button(label="Login")

        if submit:
            if (username != None):
                hashed_username = stauth.Hasher(username).generate()
                # clear the form/container and display a success message
                #placeholder.empty()
                st.success("Login successful")
                flag=True

            else:
                st.error("Login failed")

#check if username is text before proceeding (it cannot be alphanumeric)

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
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