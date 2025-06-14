import streamlit as st
import json
import sentiment_analysis as sa
import matplotlib.pyplot as plt
import pdfplumber

st.set_page_config(page_title="Earnings Call Analysis Dashboard", layout="wide")
st.title("📞 AI-Powered Earnings Call Insights (NotebookLM Style)")

# Choose input method
st.subheader("Choose Input Method")
input_mode = st.radio("Select how you want to provide the transcript:", ["Paste Text", "Upload PDF"])

transcript_text = ""

if input_mode == "Paste Text":
    transcript_text = st.text_area("Paste the con-call transcript here:", height=300)

elif input_mode == "Upload PDF":
    uploaded_pdf = st.file_uploader("Upload PDF file", type=["pdf"])
    if uploaded_pdf is not None:
        with pdfplumber.open(uploaded_pdf) as pdf:
            all_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text + "\n"
            transcript_text = all_text

# Only run LLM if text is present
if transcript_text.strip():
    with st.spinner("Analyzing transcript using GPT-4..."):
        raw = sa.analyze_sentiment(transcript_text)
        result = json.loads(raw)

    # Company & Sector
    st.subheader("🏢 Company Overview")
    c1,

