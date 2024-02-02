import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

username, authentication_status = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'Welcome *{username}*')
    switch_page("Welcome")

elif authentication_status == False:
    st.error('This UCL email address has not been granted access to this application.')

elif authentication_status == None:
    st.warning('Please enter your UCL email address.')

hide_pages(
    [
        Page(r"pages/Welcome.py", "Home", ":house:"),
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:"),
        Page(r"pages/Chatbot.py", "PyBot", ":snake:")
    ]
)