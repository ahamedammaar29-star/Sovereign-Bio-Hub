import streamlit as st
import time
import pandas as pd
import numpy as np
import random
import google.generativeai as genai
# Removing google.colab import as it's not supported on Streamlit Cloud
from aesthetic_engine import get_dynamic_assets

# --- Sovereign OS: Ultra-Elite Infrastructure Configuration ---
st.set_page_config(page_title='Sovereign OS: Bio-Hub Pro', layout='wide', initial_sidebar_state='expanded')

# --- Gemini AI Integration ---
try:
    # Using st.secrets for Streamlit Cloud compatibility
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f'Configuration Error: {e}')
    model = None

# --- System State & Persistence ---
if 'bio_credits' not in st.session_state: st.session_state.bio_credits = 5000
if 'learning_log' not in st.session_state: st.session_state.learning_log = []
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- Advanced Web UI Styling ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; }
    .stButton>button { border-radius: 20px; border: 1px solid #00ffcc; background: rgba(0, 255, 204, 0.1); color: #00ffcc; }
    </style>
""", unsafe_allow_html=True)

asset = get_dynamic_assets()

# --- Sidebar Controls ---
with st.sidebar:
    st.title('⚙℘ System Controls')
    st.info(f'Credits: {st.session_state.bio_credits} XP')

st.title('ጠ Sovereign OS: AI-Enhanced Bio-Portal')
st.caption('Evolution Level: 2.1 | Deployment: Streamlit Cloud Verified')

# --- Navigation Architecture ---
tabs = st.tabs(['ፃ Manifesto', 'ፃ AI Command Center', 'ፃ Learning Sync'])

with tabs[1]:
    st.header('ፃ Sovereign AI Neural Link')
    if not model:
        st.error('⚖ጠ GOOGLE_API_KEY missing in Streamlit Secrets.')
    else:
        for message in st.session_state.chat_history:
            role = 'ፃ Scholar' if message['role'] == 'user' else 'ፃ VC AI'
            st.markdown(f'**{role}:** {message["content"]}')

        user_input = st.chat_input('Communicate with the Venture Capitalist Core...')

        if user_input:
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            prompt = f"You are the Sovereign OS VC AI. Analyzing: {user_input}"
            response = model.generate_content(prompt)
            st.session_state.chat_history.append({'role': 'assistant', 'content': response.text})
            st.rerun()
