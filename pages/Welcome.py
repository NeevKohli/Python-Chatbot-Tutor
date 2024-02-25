import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import time

show_pages(
    [
        Page(r"pages/Welcome.py", "Home", ":house:"),
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:")
    ]
)

hide_pages(
    [
        Page(r"pages/Login.py", "Login", ":key:"),
        Page(r"pages/PyBot.py", "PyBot", ":snake:"),
    ]
)

image = Image.open('PyBot_Logo.png')

st.image(image)

st.title("Welcome to PyBot!")

st.markdown("""
The aim of PyBot is to tutor students enrolled on the ELEC0021 module on the Python programming langauge - specifically, the Week 1 Topic (Introduction to Procedural Python).
It's powered by the OpenAI API 'gpt-3.5-turbo' model (the brain behind ChatGPT) and its been trained on teaching resources :books:.
We have created PyBot with you, the students, in mind and would therefore be extremely greatful if you could use it to assist you with your learning :mortar_board:.
We encourage you to use PyBot freely and as often as you like during the beta-testing period :blush:.
Please click on 'Important Information' before chatting with PyBot!
"""
)

#Info = st.button("Important Information :octagonal_sign:")
#if Info:
#    switch_page("Important Information")