import streamlit as st
from streamlit_chat import message
import openai
from PIL import Image
from streamlit.report_thread import get_report_ctx
from openai import OpenAI
client = OpenAI()

openai.api_key="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"

from streamlit.report_thread import get_report_ctx

session_id = get_report_ctx().session_id

with st.sidebar:
    banner = st.container()
    image = Image.open('PyBot_Logo.png')
    st.image(image)
    st.title("Welcome to PyBot!")
    st.markdown("""
    The aim of PyBot is to tutor students enrolled on the ELEC0021 module on the Python programming langauge - specifically, the Week 1 Topic (Introduction to Procedural Python).
    Its powered by the OpenAI API 'gpt-3.5-turbo' model (the brain behind ChatGPT) and its been trained on teaching resources :books:.
    We have created PyBot with you, the students, in mind and would therefore be extremely greatful if you could use it to assist you with your learning :mortar_board:.
    We encourage you to use PyBot freely and as often as you like during the beta-testing period :blush:.
    Please see the 'Important Information' tab in the middle before chatting with PyBot!
    """
    )                            
    st.title("Important Information :octagonal_sign:")
    st.markdown("""     
    Disclaimer: PyBot is GDPR compliant. All users will remain anonymous and all inputs provided to PyBot will not be used for further training. Please refer to Dr. Alejandra Beghelli for further information.

    Terms of Service (ToS): PyBot should only be used for summative assessments in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). PyBot does not condone, incite and/or generates inappropriate content that violates OpenAIs usage policies (https://openai.com/policies/usage-policies).
    By using this application, you acknowledge the Disclaimer and agree to abide by the ToS.
    """
    )

st.title("PyBot :snake:")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

#Initialises session state variables, including the OpenAI model and chat messages.

# Sets the initial context for the chatbot. This provides information about the students and the Python course

#Prompt-Engineering - context

#Training file injection is fine-tuning - summary of topic 1 slide transcripts

#Chain-of-thought - guiding the chatbot on how to structure their response.

if "context" not in st.session_state:
    st.session_state.context = """
The students of ELEC0021 are studying the Python programming language starting at beginner level. 
They have learned C programming language in first year, therefore they already know at least one programming language. 
Your role is to help the students learn Python from scratch, guiding them to transfer their knowledge from C to Python. 
As a chatbot which is currently under development, you will teach the students only on the first week of term, which is 
about the basics of Python. Here are the topics taught in week 1:
    ```{Scripts.txt}```
    First of all, ask the student what level of Python knowledge they have between beginner, intermediate, advanced.  
    Beginner: knows until the Replit topic, 
    Intermediate: knows until the exception handling topic,
    Advanced: knows all topics.
    Once they have replied, you can start giving them exercises based on their knowledge level one at a time. Act as a tutor to provide the students 
    with guidance and feedback on their answers to the exercises. Tailor exercises according to the user's knowledge level. If you reckon that the user's
    knowledge level has changed over time then tailor exercises accordingly. 
    DO NOT answer queries that are not related to the Python programming language.
    In any case, DO NOT provide the solution to the exercise to the students.
    """

# Displays previous chat messages in the Streamlit app.

# Display chat messages
with st.chat_message("assistant"):
    st.write("Hi! I'm PyBot, your ELEC0021 Python programming tutor. How can I help you today?")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input and chat button ###############################################
if prompt := st.chat_input("Please enter your query..."):
    response = client.moderations.create(input=prompt)
    flagged = response['results'][0]['flagged']
    if flagged == 'false':
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("typing..."):
            # message_placeholder = st.empty()
            # full_response = ""
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": st.session_state.context},
                    {"role": "user", "content": prompt},
                ],
            )

        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

        #Displays the user's input and the assistant's response in the Streamlit app.

        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message["content"])
    else:
        with st.chat_message("assistant"):
            st.write("PyBot does not engage with inappropriate language.")

            st.write("You have now been blocked and your responses will not be registered.")
############################################################################