import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title
import openai
from PIL import Image
import streamlit_authenticator as stauth
from openai import OpenAI
client = OpenAI()

openai.api_key="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"

#Login page - user enters credentials (username and/or password) to access conversation history (archived from previous sessions)
#Hash (encrypt) them for user privacy and security before implementing end-user IDs for OpenAI to monitor via the moderation endpoint tool
#better than Session IDs which are only valid for a single session so users cannot access their conversation history

# Create an empty container
placeholder = st.empty()
flag=False

while flag==False:
    # Insert a form in the container
    with placeholder.form("login"):
        #Single
        st.markdown(":wave:")
        username = st.text_input("Username")
        submit = st.form_submit_button("Login")

    if username != None:
        hashed_username = stauth.Hasher(username).generate()
        # clear the form/container and display a success message
        placeholder.empty()
        st.success("Login successful")
        flag=True

    else:
        st.error("Login failed")

#check if username is text before proceeding (it cannot be alphanumeric)

#To maximise throughput, parallel processing needs to be impemented to handle
#large volumes of parallel API calls/requests via throttling so that rate limits are not exceeded


#light and dark mode toggles
dark = '''
<style>
    .stApp {
    background-color: black;
    }
</style>
'''

light ='''
<style>
    .stApp {
    background-color: white;
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

container1 = st.container(border=True)
container1.write("This is inside the container")
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

expander = st.expander("Important Information :octagonal_sign:")
expander.write(\"\"\"
    Disclaimer: PyBot is GDPR compliant. All users will remain anonymous and all inputs provided to PyBot will not be used for further training. Please refer to Dr. Alejandra Beghelli for further information.

    Terms of Service (ToS): PyBot should only be used for summative assessments in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). PyBot does not condone, incite and/or generates inappropriate content that violates OpenAIs usage policies (https://openai.com/policies/usage-policies).
    By using this application, you acknowledge the Disclaimer and agree to abide by the ToS.
    \"\"\")


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
    response = client.moderations.create(input=prompt)
    flagged = response['results'][0]['flagged']

    if flagged == 'false':
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
            response = client.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": st.session_state.context},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                user=hashed_username,
            )

        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

        #Displays the user's input and the assistant's response in the Streamlit app.

        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message["content"])
    else:
        with st.chat_message("assistant"):
            st.write("PyBot does not engage with inappropriate language.")
            st.write("You will now been blocked from interacting with PyBot.")
            st.write("If you believe this is a mistake then please contact the developers.")
            st.stop()