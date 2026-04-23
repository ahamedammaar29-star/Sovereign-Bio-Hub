import streamlit as st
import time
import pandas as pd
import numpy as np
import io
import PyPDF2
import google.generativeai as genai
from aesthetic_engine import get_dynamic_assets

# --- Sovereign OS: Production Configuration ---
st.set_page_config(page_title='Sovereign OS: Bio-Hub Pro', layout='wide')

# --- State Management ---
if 'bio_credits' not in st.session_state:
    st.session_state.bio_credits = 5000
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- AI Core Initialization (Cloud-Native) ---
try:
    # LOOK HERE: This line retrieves the secret via Streamlit Cloud Secrets
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ System Alert: AI Core configuration missing. Please verify your Cloud Secrets.")
    model = None

# --- Dashboard Interface ---
st.title('ጠ Sovereign OS: Neural Scholar Pro')

tabs = st.tabs(['ፃ AI Command Center', 'ፃ Learning Sync'])

with tabs[0]:
    st.header('Sovereign AI Neural Link')
    for msg in st.session_state.chat_history:
        st.chat_message(msg['role']).write(msg['content'])

    if user_input := st.chat_input('Consult the Venture AI...'):
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        st.chat_message('user').write(user_input)

        if model:
            try:
                response = model.generate_content(f"You are a VC AI. {user_input}")
                st.session_state.chat_history.append({'role': 'assistant', 'content': response.text})
                st.chat_message('assistant').write(response.text)
            except Exception as api_err:
                st.error(f"Neural Sync Error: {api_err}")

with tabs[1]:
    st.header('ፃ Learning & Data Ingestion')
    file = st.file_uploader("Upload Research Data (PDF/TXT)", type=['pdf', 'txt'])

    if file:
        if st.button('Initialize Deep Analysis'):
            with st.status('Extracting Logical Vectors...'):
                extracted_text = ""
                if file.type == "text/plain":
                    extracted_text = str(file.read(), "utf-8")
                else:
                    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    extracted_text = " ".join([p.extract_text() for p in reader.pages])

                if model:
                    prompt = f"Summarize research data and identify ROI potential: {extracted_text[:4000]}"
                    analysis = model.generate_content(prompt)
                    st.subheader("VC Intelligence Report")
                    st.write(analysis.text)
                    st.session_state.bio_credits += 300
                    st.success("Knowledge persistent. +300 XP added to profile.")
