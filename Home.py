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
        Page(r"pages/Welcome.py", "Welcome", ":house:"),
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:"),
        Page(r"pages/PyBot.py", "PyBot", ":snake:"),
    ]
)

switch_page("Login")
