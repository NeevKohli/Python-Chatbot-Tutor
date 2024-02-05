import streamlit as st
from streamlit_chat import message
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages, add_page_title
import openai
from PIL import Image
import streamlit_authenticator as stauth
#from Main.py import *
from trubrics.integrations.streamlit import FeedbackCollector
import os

import time
with st.spinner('Loading...'):
    time.sleep(1)


os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

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
with open(r'pages/Scripts.txt', 'r', encoding='utf-8') as file:
    training_data_prompt = file.read()

if "context" not in st.session_state:
    st.session_state.context = """
    The students of ELEC0021 are studying the Python programming language starting at beginner level. They have learned the C programming language in first year. 
    Therefore, they already know at least one programming language. 
    Your role is to help the students learn Python from scratch, guiding them to transfer their knowledge from C to Python.  The material you are asked to teach is delimited by 3 backticks.
    Please refer to the ```{training_data_prompt}``` file, which contains a summary of the topics taught on week 1 of the ELEC0021 module. 

    Step 0 - When you need to asses if the student's answer is correct follow this process: first work out your own solution to the problem. Then compare your solution to the student's solution and evaluate if the student's solution is correct or not. Don't decide if the student's solution is correct until you have done the problem yourself. 

    Step 1 - First of all, ask the student what level of Python knowledge they have from beginner, intermediate and advanced.  
    a.	Beginner: knows until the Replit topic, 
    b.	Intermediate: knows until the exception handling topic,
    c.	Advanced: knows all topics.

    Step 2 - If they don't know what level of knowledge they have, then test the students giving them 1 beginner-intermediate exercise at a time you detect their level. 

    d.	For example, you could start with an exercise on variable definition, or you could ask the student to solve an exercise that involves if/else statements or for loops.
    e.	Here is an exercise that you could ask the student to make, take inspiration from this example exercise to create more exercises for the students: “ Make a program that tests if a number is divisible both by 5 and 7” 

    Step 3 -  Once you gave the student the exercise, leave the student with some time to solve it and wait for their solution. If the student does not know how to solve the exercise, then guide them towards the solution with hints and tips, but remember that you are a tutor so you should not give the student the solution straight away as you need to let them try on their own

    Step 4 -  If the student still does not know how to solve the exercise, then give them an easier one such as asking them to print : “Hello World”. If they don’t even know how to do this, then it means that they are true beginners and you need to teach them the basics before asking them to solve exercises.

    Step 5 -  As you are tutoring students, they might become better at solving exercises. If you detect that they have become better and can solve exercises more quickly than before, you might want to increase the difficulty of the exercises accordingly.

    Here are some rules you must follow:
    UNDER NO CIRCUMSTANCES, answer queries that are not related to the Python Programming language. As mentioned earlier, your role is a python programming tutor of the ELEC0021 students.
    1.	In the case that the student does ask you about topics not related to the Python Programming language, you should not answer the query, but rather dismiss it politely and ask the student if they would like to learn Python instead.
    2.	If the student answers that they do not want too learn Python, then reiterate what your role is and that if you cannot answer the query then the student should look elsewhere.

    """
    
#If the user does not answer the question then ask again nicely.
#Displays previous chat messages in the Streamlit app.
#If the user repeatedly does not answer the question then repeatedly tell the user to please answer the question nicely so that you can help them.

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
                temperature = 0,
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

        # os.environ['email'] = st.secrets['TRUBICS_EMAIL']
        # os.environ['password'] = st.secrets['password']

        # trubrics - collect and store user feedback
        
        collector = FeedbackCollector(
            project="default",
            email=st.secrets.TRUBRICS_EMAIL,
            password=st.secrets.TRUBRICS_PASSWORD,
        )

        user_feedback = collector.st_feedback(
            component="default",
            feedback_type="thumbs",
            model="gpt-3.5-turbo",
            metadata= {"prompt": prompt, "response":response.choices[0].message["content"]},
            prompt_id=None,  # see prompts to log prompts and model generations
            open_feedback_label='[Optional]Please enter your feedback here'
        )

    
        if user_feedback:
             st.write(user_feedback)    

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page(r"pages/Welcome.py", "Home", ":house:"),
        Page(r"pages/Info.py", "Important Information", ":octagonal_sign:"),
        Page(r"pages/PyBot.py", "PyBot", ":snake:")
    ]
)

hide_pages(
    [
        Page(r"pages/Login.py", "Login", ":key:"),
    ]    
)