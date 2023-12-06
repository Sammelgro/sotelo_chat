import json
import streamlit as st
import replicate
import os
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner

# App title
st.set_page_config(page_title="🤖Control Chat")

#Lottie
lottie_url = "https://lottie.host/ed9f7d11-d2f6-44c5-bf79-80645fcd179f/guP07rzLPB.json"

#Model
llm = 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3'
temperature = 0.9
top_p = 0.6

#Replicate ID
replicate_api = "r8_2kkTh4tEB2ynAx4rm9r72NnC90VpoTt4PGU2v"
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Sidebar
with st.sidebar:
    st.title('🤖 Control Chat (v2.0.R.E)')
    '''This is an Experimental Chatbot. Made by Samuel A. Melendez. In collaboration with Dr. Carlos Sotelo and Dr. David Sotelo. The Chatbot uses the Llama 2 model by Meta and the Streamlit UI.'''
    st_lottie(lottie_url, key="user")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#Chat History
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)