import openai
import streamlit as st
import os
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import  Pinecone
from langchain.text_splitter import TokenTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message
from utils import *
import pinecone
from PIL import Image

pdfs = [file for file in os.listdir() if 'pdf' in file]

page_list = []
for pdf in pdfs:
    pdf_path = f"{pdf}"
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    page_list.append(pages)

flat_list = [item for sublist in page_list for item in sublist]

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)

texts = text_splitter.split_documents(flat_list)

#@st.cache_data
#def ada_embeddings():
  #  OpenAIEmbeddings(openai_api_key="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")
 #   return
#
#embeddings = ada_embeddings()

embeddings = OpenAIEmbeddings(openai_api_key="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")

@st.cache_resource
def vdb_connection():
    pinecone.init(      
    api_key='ab5a11d1-28d4-4c93-a1a4-ffeb07fca4c5',      
    environment='gcp-starter'      
    )  
    return  

vdb = vdb_connection()

index_name='pybot'

index = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

@st.cache_data
def get_similiar_docs(query,k=1,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

tab1, tab2, tab3  = st.tabs([
    "About :mag:", 
    "Important Information :octagonal_sign:",
    "PyBot :snake:"]
    )

with tab1:
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

with tab2:
    st.title("Important Information")
    st.markdown("""     
    Disclaimer: PyBot is GDPR compliant. All users will remain anonymous and all inputs provided to PyBot will not be used for further training. Please refer to Dr. Alejandra Beghelli for further information.
    
    Terms of Service (ToS): PyBot should only be used for summative assessments in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). PyBot does not condone, incite and/or generates inappropriate content that violates OpenAIs usage policies (https://openai.com/policies/usage-policies).')
    By using this application, you acknowledge the Disclaimer and agree to abide by the ToS.
    """
    )

with tab3:
    st.title("PyBot")
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    if 'buffer_memory' not in st.session_state:
        st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)

    system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
    and if the answer is not contained within the text below, say 'I don't know'""")

    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
    
    response_container = st.container()
    textcontainer = st.container()
  
    with textcontainer:
        query = st.text_input("Query: ", key="input")
        context = "You are a tutor for students studying the Python programming language"
    with response_container:
        if st.session_state['responses']:
            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

#    @st.cache_data
 #   def llm():
  #      ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")
#
 #   gpt=llm()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")

    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

    if query:
        with st.spinner("typing..."):
#            filter = openai.Moderations.create(query)
 #           if filter.results[0].flagged == 'false':
            response = conversation.predict(input=f"Context:\n{context} \n\n Query:\n{query}")
  #          else:
   #             st.write("I'm sorry but I couldn't understand your question. Could you please try again?")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

    @st.cache_data
    def query_refiner(conversation, query):
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return response['choices'][0]['text']

    @st.cache_data
    def find_match(input):
        input_em = model.encode(input).tolist()
        result = index.query(input_em, top_k=2, includeMetadata=True)
        return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

    @st.cache_data
    def get_conversation_string():
        conversation_string = ""
        for i in range(len(st.session_state['responses'])-1):        
            conversation_string += "User: "+st.session_state['requests'][i] + "\n"
            conversation_string += "PyBot: "+ st.session_state['responses'][i+1] + "\n"
        return conversation_string

#if "openai_model" not in st.session_state:
 #   st.session_state["openai_model"] = "gpt-3.5-turbo"

#if "messages" not in st.session_state:
 #   st.session_state.messages = []

#for message in st.session_state.messages:
 #   with st.chat_message(message["role"]):
  #      st.markdown(message["content"])

#if prompt := st.chat_input("What would you like to ask PyBot?"):
 #   st.session_state.messages.append({"role": "user", "content": prompt})
  #  with st.chat_message("user"):
   #     st.markdown(prompt)

    #with st.chat_message("assistant"):
     #   message_placeholder = st.empty()
      #  full_response = ""
       # for response in openai.ChatCompletion.create(
        #    model=st.session_state["openai_model"],
         #   messages=[
          #      {"role": m["role"], "content": m["content"]}
           #     for m in st.session_state.messages
            #],
            #stream=True,
        #):
         #   full_response += response.choices[0].delta.get("content", "")
          #  message_placeholder.markdown(full_response + "▌")
        #message_placeholder.markdown(full_response)
    #st.session_state.messages.append({"role": "assistant", "content": full_response})
