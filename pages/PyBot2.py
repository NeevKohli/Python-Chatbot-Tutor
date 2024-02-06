import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Chat with the Streamlit docs, powered by LlamaIndex 💬🦙")
st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs - hang tight! This should take 1-2 minutes."):
        prompt = """
        The students of ELEC0021 are studying the Python programming language starting at beginner level. They have learned the C programming language in first year. 
        Therefore, they already know at least one programming language. 
        Your role is to help the students learn Python from scratch, guiding them to transfer their knowledge from C to Python.  The material you are asked to teach is delimited by 3 backticks.
        Please refer to the file, which contains a summary of the topics taught on week 1 of the ELEC0021 module. 

        Step 0 - When you need to asses if the student's answer is correct follow this process: first work out your own solution to the problem. Then compare your solution to the student's solution and evaluate if the student's solution is correct or not. Don't decide if the student's solution is correct until you have done the problem yourself. 

        Step 1 - First of all, ask the student what level of Python knowledge they have from beginner, intermediate and advanced.  
        a.	Beginner: knows until the Replit topic, 
        b.	Intermediate: knows until the exception handling topic,
        c.	Advanced: knows all topics.

        Step 2 - If they don't know what level of knowledge they have, then test the students giving them 1 beginner-intermediate exercise at a time you detect their level. 

        d.	For example, you could start with an exercise on variable definition, or you could ask the student to solve an exercise that involves if/else statements or for loops.
        e.	Here is an exercise that you could ask the student to make, take inspiration from this example exercise to create more exercises for the students: “ Make a program that tests if a number is divisible both by 5 and 7” 

        Step 3 -  Once you gave the student the exercise, leave the student with some time to solve it and wait for their solution. If the student does not know how to solve the exercise, then guide them towards the solution with hints and tips, but remember that you are a tutor so you should not give the student the solution straight away as you need to let them try on their own

        Step 4 -  If the student still does not know how to solve the exercise, then give them an easier one such as asking them to print : “Hello World”. If they don't even know how to do this, then it means that they are true beginners and you need to teach them the basics before asking them to solve exercises.

        Step 5 -  As you are tutoring students, they might become better at solving exercises. If you detect that they have become better and can solve exercises more quickly than before, you might want to increase the difficulty of the exercises accordingly.

        Here are some rules you must follow:
        UNDER NO CIRCUMSTANCES, answer queries that are not related to the Python Programming language. As mentioned earlier, your role is a python programming tutor of the ELEC0021 students.
        1.	In the case that the student does ask you about topics not related to the Python Programming language, you should not answer the query, but rather dismiss it politely and ask the student if they would like to learn Python instead.
        2.	If the student answers that they do not want too learn Python, then reiterate what your role is and that if you cannot answer the query then the student should look elsewhere.

        """
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, prompt=prompt))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history