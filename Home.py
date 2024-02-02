import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title
from PIL import Image
import streamlit_authenticator as stauth

#Add Alejandra's, Arnas', Iason's and the 5 students email later (10 testers in total of which 2 are white-box and 8 are black-box)
emails = ['zceenko@ucl.ac.uk','zceemc0@ucl.ac.uk']

hashed_emails = stauth.Hasher(emails).generate()

authenticator = stauth.authenticate(hashed_emails,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)

username, authentication_status = authenticator.login('Login','main')

if st.session_state['authentication_status']:
    st.write('Welcome *%s*' % (st.session_state['username']))
    switch_page("Welcome")

elif st.session_state['authentication_status'] == False:
    st.error('The UCL email address entered has not been granted access to this application.')

elif st.session_state['authentication_status'] == None:
    st.warning('Please enter your username and UCL email address.')