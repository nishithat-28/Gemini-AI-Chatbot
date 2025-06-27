import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument


st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://img.freepik.com/free-vector/digital-dark-wavy-background_23-2148388254.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .stButton > button {
        background-color: #DD0000;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }

    .stTextInput > div > div > input {
        background-color: #FFFFFF; 
        color: #00154D;
    }

    h1 {
        color: white;
        text-align: center;
        font-family : Verdana, sans-serif;
        font-weight: 100;
    }
    h2 {
        color: white;
        text-align: center;
        font-family : Verdana, sans-serif;
        font-weight: 100;
    }
    h3 {
        color: white;
        text-align: center;
        font-family : Verdana, sans-serif;
        font-weight: 100
    }

    
    
    </style>
    """,
    unsafe_allow_html=True
)

st.write("\n" * 8)
st.title("Welcome to our Community")
st.subheader("Learn.Lead.Live")
st.write("\n" * 3)

with st.sidebar:
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    st.subheader("API Key")
    st.session_state.api_key = st.text_input("Enter your Gemini API Key", type="password", key="api_key_input")
    

if not st.session_state.api_key:
    st.warning("Please enter your Gemini API key in the sidebar.")

try:
    genai.configure(api_key=st.session_state.api_key)
    model = genai.GenerativeModel(model_name='models/gemini-2.0-flash-lite') # gemini-2.0-flash-lite, gemini-1.5-pro
    if 'chat' not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
    
    qn = st.chat_input("Type Something:", key="home_input")
    if qn:
        st.chat_message("user").write(qn)
        with st.spinner("Generating response..."):
            response = st.session_state.chat.send_message(qn)
        st.chat_message("ai").write(response.text)
        

except Exception as e:
    st.error(f"❌ Failed to initialize Gemini model: {e}")



    