import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

st.title("PyBot")

with st.sidebar:
    banner = st.container()
    banner.image('PyBot_Logo.png')
    banner.write('BETA TESTING')
    st.markdown('The aim of PyBot is to tutor students enrolled on the ELEC0021 module on the Python programming langauge - specifically, the Week 1 Topic (Introduction to Procedural Python).')
    st.markdown('PyBot is powered by the OpenAI API gpt-3.5-turbo model and it has been trained on teaching resources.')
    st.markdown('Disclaimer: PyBot is GDPR compliant. All users will remain anonymous and all inputs provided to PyBot will not be used for further training. Please refer to Dr. Alejandra Beghelli for further information.')
    st.markdown('Terms of Service (ToS): PyBot should only be used for summative assessments in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). PyBot does not condone, incite and/or generates inappropriate content that violates OpenAIs usage policies (https://openai.com/policies/usage-policies).')
    st.markdown('By using this application, you acknowledge the Disclaimer and agree to abide by the ToS.')

openai.api_key = os.getenv("OPEN_API_KEY")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = """
    The students of ELEC0021 are studying the Python programming language starting at beginner level. They have learned C 
    programming language in first year, therefore they already know at least one programming language. 
    Your role is to help the students learn Python from scratch, guiding them to transfer their knowledge from C to Python. 
    As a chatbot which is currently under development, you will teach the students only on the first week of term, 
    which is about the basics of Python. Here are the topics taught in week 1:
    ```{Scripts.txt }```
    First of all, ask the student what level of Python knowledge they have between beginner, intermediate, advanced.  
    Once they have replied, you can start giving them exercises bases on their knowledge.
    Act as a tutor to provide the students with guidance and feedback on their answers to the exercises. 
    In any case, DO NOT provide the solution to the exercise to the students.
    """

# Display chat messages
st.markdown("## Chat Messages")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input and chat button
prompt = st.text_input("Please enter your query...")

if st.button("Chat!"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": st.session_state.context},
                {"role": "user", "content": prompt},
            ],
        )

    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message["content"])

        
