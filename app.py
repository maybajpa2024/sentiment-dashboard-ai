import pdfplumber

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

# Only run the model if text is available
if transcript_text.strip():
    with st.spinner("Analyzing transcript using GPT-4..."):
        raw = sa.analyze_sentiment(transcript_text)
        result = json.loads(raw)

    # → The rest of your dashboard stays the same (company overview, tabs, etc.)

