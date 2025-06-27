import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument
import time

st.set_page_config(
    page_title="Chatbot",
    page_icon=":speech_balloon:",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    h1 {
        text-align: center;
        font-family : Verdana, sans-serif;
        font-weight: 100;
    }
    h2 {
        text-align: center;
        font-family : Verdana, sans-serif;
        font-weight: 100;
    }
    h3 {
        text-align: center;
        font-family : Verdana, sans-serif;
        font-weight: 100
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to our Community")
st.subheader("Learn.Lead.Live")

with st.sidebar:
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    st.subheader("API Key")
    st.session_state.api_key = st.text_input("Enter your Gemini API Key", type="password", key="api_key_input")

    if st.button("Clear Chat"):
        st.session_state.messages = []

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)
try:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel(model_name='models/gemini-2.0-flash-lite') # gemini-2.0-flash-lite, gemini-1.5-pro
    if 'chat' not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])
    
    qn = st.chat_input("Type Something ...", key="home_input")
    if qn and qn.strip():
        if not st.session_state.api_key:
            st.warning("Please enter your Gemini API key in the sidebar.")
        else:
            st.chat_message("user").write(qn)
            st.session_state.messages.append({"role":"user", "content":qn})
            with st.spinner("Generating response..."):
                response = st.session_state.chat.send_message(qn)
            st.chat_message("ai").write_stream(stream_data(response.text))
            st.session_state.messages.append({"role":"ai", "content":response.text})
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini model: {e}")
