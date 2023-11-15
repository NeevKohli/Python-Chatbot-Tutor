!pip install openai streamlit

import openai
import streamlit as st

st.title("PyBot")

with st.sidebar:
 banner = st.container()
 banner.image('PyBot_Logo.png')
 banner.write('BETA TESTING')
 st.markdown('The aim of PyBot is to tutor students enrolled on the ELEC0021 module on the Python programming langauge - specifically, the Week 1 Topic (Introduction to Procedural Python).')
 st.markdown('PyBot is powered by the OpenAI API gpt-3.5-turbo model and it has been trained on teaching resources.')
 st.markdown('Disclaimer: PyBot is GDPR compliant. All users will remain anonymous and all inputs provided to PyBot will not be used for further training. Please refer to Dr. Alejandra Beghelli for further information.')
 st.markdown('Terms of Service (ToS): PyBot should only be used for summative assessments in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). PyBot does not condone, incite and/or generates inappropriate content that violates OpenAIs usage polices. <Add OpenAI link>')
 st.markdown('By using this application, you acknowledge the Disclaimer and agree to abide by the ToS.')
