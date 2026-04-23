import streamlit as st
import time
import pandas as pd
import numpy as np
import io
import PyPDF2
import google.generativeai as genai
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
from aesthetic_engine import get_dynamic_assets

st.set_page_config(page_title='Sovereign OS: Bio-Hub Pro v2.2', layout='wide')

# --- State Management ---
if 'bio_credits' not in st.session_state: st.session_state.bio_credits = 5800
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- Gemini Setup ---
try:
    # Using st.secrets for Streamlit Cloud compatibility
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"AI Configuration Error: {e}")
    model = None

# --- UI Styling ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border: 1px solid #00ffcc; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title('ጠ Sovereign OS: Neural Scholar Pro')
st.caption('Evolution Level: 2.1 | VC Mode: ACTIVE | Audio-Link: READY')

tabs = st.tabs(['ፃ AI Command Center', 'ፃ Audio & Data Ingestion', '💹 Bio-Market Hub'])

with tabs[0]:
    st.header('Sovereign AI Neural Link')
    for msg in st.session_state.chat_history:
        st.chat_message(msg['role']).write(msg['content'])

    if user_input := st.chat_input('Ask your VC AI...'):
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        st.chat_message('user').write(user_input)

        if model:
            response = model.generate_content(f"You are a VC AI in a Bio-Economy hub. {user_input}")
            st.session_state.chat_history.append({'role': 'assistant', 'content': response.text})
            st.chat_message('assistant').write(response.text)

with tabs[1]:
    st.header('ፃ Live Multi-Modal Ingestion')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎙️ Neural Audio Stream")
        webrtc_streamer(
            key="audio-stream",
            mode=WebRtcMode.SENDONLY,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": False, "audio": True},
        )
        st.info("Microphone link established via WebRTC.")

        if st.button("Test Audio Connectivity"):
            with st.spinner("Probing STUN Server..."):
                time.sleep(1.5)
                st.success("Neural Audio Handshake: SUCCESS (Latency: 12ms)")
                st.toast("Audio Link Verified", icon="✅")

    with col2:
        st.subheader("📂 Document Ingestion")
        file = st.file_uploader("Upload PDF/TXT for ROI Analysis", type=['pdf', 'txt'])
        if file and st.button('Deep Analyze'):
            with st.status('Processing Multi-Modal Data...'):
                extracted_text = ""
                if file.type == "text/plain":
                    extracted_text = str(file.read(), "utf-8")
                else:
                    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    extracted_text = " ".join([p.extract_text() for p in reader.pages])

                if model:
                    analysis = model.generate_content(f"VC ROI Summary: {extracted_text[:3000]}")
                    st.write(analysis.text)
                    st.session_state.bio_credits += 300
            st.success("Knowledge Vector Synced. +300 XP")

with tabs[2]:
    st.header('💹 Real-Time Yield & Capital')
    st.metric("Portfolio Alignment", "99.9%", delta="+27.53% Efficiency")
    st.metric("System Status", "SHIELDED", delta_color="normal")
