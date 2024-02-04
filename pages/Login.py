import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

show_pages(
    [
        Page(r"pages/Login.py", "Login", ":key:"),
    ]
)

hide_pages(
    [
        Page(r"pages/Welcome.py", "Home", ":house:"),
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:"),
        Page(r"pages/PyBot.py", "PyBot", ":snake:")
    ]
)

with open(r"pages/config.yml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()

if st.session_state["authentication_status"]:
    show_pages(
    [
        Page(r"pages/Login.py", "Login", ":key:"),
        Page(r"pages/Welcome.py", "Home", ":house:"),
    ]
)
    hide_pages(
    [
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:"),
        Page(r"pages/PyBot.py", "PyBot", ":snake:"),
    ]
)
    switch_page("Home")

elif st.session_state["authentication_status"] is False:
    st.error('You have not been granted access to this application. Please try again with different credentials.')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your credentials.')