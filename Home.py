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
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    st.write(f'Welcome *{st.session_state["name"]}*')
    switch_page("Welcome")

elif st.session_state["authentication_status"] is False:
    st.error('This UCL email address has not been granted access to this application.')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your UCL email address.')
