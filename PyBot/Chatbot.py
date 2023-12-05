import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title
import openai
from PIL import Image
import streamlit_authenticator as stauth
#from Main.py import *

openai.api_key="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"

#light and dark mode toggles
dark = '''
<style>
    .stApp {
    background-color: black;
    color: white;
    }
</style>
'''

light ='''
<style>
    .stApp {
    background-color: white;
    color: black;
    }
</style>
'''
st.markdown(light, unsafe_allow_html=True)

# Create a toggle button
toggle = st.button(":white_large_square::left_right_arrow::black_large_square:")

# Use a global variable to store the current theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Change the theme based on the button state
if toggle:
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"

# Apply the theme to the app
if st.session_state.theme == "dark":
    st.markdown(dark, unsafe_allow_html=True)
else:
    st.markdown(light, unsafe_allow_html=True)

#To maximise throughput, parallel processing needs to be impemented to handle
#large volumes of parallel API calls/requests via throttling so that rate limits are not exceeded

st.title("PyBot :snake:")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

#Initialises session state variables, including the OpenAI model and chat messages.

#Sets the initial context for the chatbot. This provides information about the students and the Python course

#Prompt-Engineering - context

#Training file injection is fine-tuning - summary of topic 1 slide transcripts

#Chain-of-thought - guiding the chatbot on how to structure their response.

if "context" not in st.session_state:
    st.session_state.context = """
The students of ELEC0021 are studying the Python programming language starting at beginner level. 
They have learned the C programming language in first year. Therefore, they already know at least one programming language. 
Your role is to help the students learn Python from scratch, guiding them to transfer their knowledge from C to Python. 
As a chatbot which is currently under development, you will teach the students only on the first week of term, which is 
about the basics of Python. Here are the topics taught in week 1:
    ```{Scripts.txt}```
    First of all, ask the student what level of Python knowledge they have from beginner, intermediate and advanced.  
    Beginner: knows until the Replit topic, 
    Intermediate: knows until the exception handling topic,
    Advanced: knows all topics.
    If the user does not answer the question then ask again nicely.
    If the user repeatedly does not answer the question then repeatedly tell the user to please answer the question nicely so that you can help them.
    Once they have replied, you can start giving them exercises based on their knowledge level one at a time. Act as a tutor to provide the students 
    with guidance and feedback on their answers to the exercises. Tailor exercises according to the user's knowledge level. If you feel that the user's
    knowledge level has changed over time, then tailor exercises accordingly. 
    DO NOT answer queries that are not related to the Python programming language.
    In any case, DO NOT provide the exercise solutions to the students.
    """

#Displays previous chat messages in the Streamlit app.

#PyBot outputs first message
with st.chat_message("assistant"):
    st.write("Hi! I'm PyBot, your ELEC0021 Python programming tutor. How can I help you today?")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#User's message is input
if prompt := st.chat_input("Please enter your query..."):

    #Checking if user's prompt is not flagged as violating OpenAI's usage policies
    #response = openai.moderations.create(input=prompt)
    #flagged = response['results'][0]['flagged']

    #if flagged == 'false':
        st.session_state.messages.append({"role": "user", "content": prompt})

        #User message is displayed
        with st.chat_message("user"):
            st.markdown(prompt)

        #NLP text preprocessing (reduces tokens used)


        #Prompt injection attack prevention


        #Displaying to user that PyBot's response is loading/being generated
        with st.spinner("typing..."):
            #message_placeholder = st.empty()
            #full_response = ""
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": st.session_state.context},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                #user=hashed_username,
            )

        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

        #Displays the user's input and the assistant's response in the Streamlit app.

        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message["content"])
    #else:
        #with st.chat_message("assistant"):
         #   st.write("PyBot does not engage with inappropriate language.")
          #  st.write("You will now been blocked from interacting with PyBot.")
           # st.write("If you believe this is a mistake then please contact the developers.")
            #st.stop()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("Home.py", "Home", ":house:"),
        Page("Info.py", "Important Information", ":octagonal_sign:"),
        Page("Chatbot.py", "PyBot", ":snake:")
    ]
)
