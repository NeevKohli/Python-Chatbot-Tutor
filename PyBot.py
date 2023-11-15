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
 st.markdown('Terms of Service (ToS): PyBot should only be used for summative assessments in accordance with UCL policy (https://www.ucl.ac.uk/students/exams-and-assessments/assessment-success-guide/engaging-ai-your-education-and-assessment). PyBot does not condone, incite and/or generates inappropriate content that violates OpenAIs usage policies (https://openai.com/policies/usage-policies).')
 st.markdown('By using this application, you acknowledge the Disclaimer and agree to abide by the ToS.')

openai.api_key = "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"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Please enter your query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
