import streamlit as st
import time
import pandas as pd
import numpy as np
import io
import PyPDF2
import google.generativeai as genai
from google.colab import userdata
from aesthetic_engine import get_dynamic_assets

st.set_page_config(page_title='Sovereign OS: Bio-Hub Pro', layout='wide')

# --- State Management ---
if 'bio_credits' not in st.session_state: st.session_state.bio_credits = 5000
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- Gemini Setup ---
try:
    genai.configure(api_key=userdata.get('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
except: model = None

# --- UI Assets ---
asset = get_dynamic_assets()

# --- App Layout ---
st.title('ጠ Sovereign OS: Neural Scholar Pro')

tabs = st.tabs(['ፃ AI Command Center', 'ፃ Learning Sync'])

with tabs[0]:
    st.header('Sovereign AI Neural Link')
    for msg in st.session_state.chat_history:
        st.chat_message(msg['role']).write(msg['content'])

    if user_input := st.chat_input('Ask your VC AI...'):
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        st.chat_message('user').write(user_input)

        response = model.generate_content(f"You are a VC AI. {user_input}")
        st.session_state.chat_history.append({'role': 'assistant', 'content': response.text})
        st.chat_message('assistant').write(response.text)

with tabs[1]:
    st.header('ፃ Learning & Ingestion')
    file = st.file_uploader("Upload PDF or TXT", type=['pdf', 'txt'])

    if file:
        if st.button('Deep Analyze Document'):
            with st.status('Extracting data...'):
                extracted_text = ""
                if file.type == "text/plain":
                    extracted_text = str(file.read(), "utf-8")
                else:
                    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    extracted_text = " ".join([p.extract_text() for p in reader.pages])

                # Send to Gemini
                prompt = f"Summarize the following research data and identify the ROI potential: {extracted_text[:4000]}"
                analysis = model.generate_content(prompt)

            st.subheader("VC Analysis Report")
            st.write(analysis.text)
            st.session_state.bio_credits += 300
            st.success("Neural extraction complete. +300 XP awarded.")
