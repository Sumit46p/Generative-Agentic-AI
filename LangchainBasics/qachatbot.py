import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os

## Page config

st.set_page_config(page_title = "Simple Langchain Chatbot with Groq", page_icon = "🤖")

## Title
st.title("Simple Langchain Chat with Groq")
st.markdown("Learn Langchain basics with Groq's ultra fast interface")


with st.sidebar:
    st.header("Settings")
    
    ## API key
    api_key = st.text_input("Groq API Key", type = "password", help ="Get Free API key at console.groq.com")

    ## Model Selection
    model_name = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile"],
        index = 0
    )

    ## Clear
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

## Initialize LLM 
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None
    
    llm = ChatGroq(groq_api_key=api_key, model_name = model_name, temperature = 0.7, streaming = True)


## Create prompt template

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant powered by Groq. Answer question clearly and concisely."),
        ("user","{question}")
    ])

    ## Create Chain
    chain = prompt| llm | StrOutputParser()
    return chain

## get chain

chain = get_chain(api_key,model_name)

if not chain:
    st.warning("Invalid API")

else:
    # Display Chat Message
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    ## chat input
    if question:= st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role":"user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        ## Generate Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                #Stream response from Groq
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "")
                
                message_placeholder.markdown(full_response)

                ## Add to history
                st.session_state.messages.append({"role":"assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error: {str(e)}")

