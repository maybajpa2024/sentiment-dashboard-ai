import streamlit as st
import json
import sentiment_analysis as sa
import matplotlib.pyplot as plt
import pdfplumber

st.set_page_config(page_title="Earnings Call Analysis Dashboard", layout="wide")
st.title("📞 AI-Powered Earnings Call Insights (NotebookLM Style)")

# --- Input Mode Selection ---
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

# --- GPT Analysis Trigger ---
if transcript_text.strip():
    with st.spinner("Analyzing transcript using GPT-4..."):
        raw = sa.analyze_sentiment(transcript_text)
        result = json.loads(raw)

    # --- Company & Sector ---
    st.subheader("🏢 Company Overview")
    c1, c2 = st.columns(2)
    c1.metric("Company", result.get("company_name", "N/A"))
    c2.metric("Sector", result.get("sector_name", "N/A"))

    st.markdown("---")

    # --- Dashboard Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Sentiment", "🗣️ Key Quotes", "✅ Business Insights", "📈 Trends & Mix"])

    with tab1:
        st.subheader("Sentiment Overview")
        st.info(f"🧠 Overall Tone: **{result['overall_sentiment']}**")

        labels = list(result["sentiment_breakdown"].keys())
        sizes = list(result["sentiment_breakdown"].values())
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

    with tab2:
        st.subheader("Key Quotes with Tone")
        for quote in result["key_quotes"]:
            sentiment = quote["sentiment"]
            color = "🟢" if "Optimistic" in sentiment else "🟡" if "Neutral" in sentiment else "🔴"
            st.markdown(f"{color} **{sentiment}**: “{quote['quote']}”")

    with tab3:
        st.subheader("Top Business Takeaways")
        for i, pt in enumerate(result.get("key_takeaways", []), 1):
            st.markdown(f"**{i}.** {pt}")

    with tab4:
        st.subheader("Industry Trends")
        for i, trend in enumerate(result.get("industry_trends", []), 1):
            st.markdown(f"**{i}.** {trend}")

        st.subheader("Product/Segment Commentary")
        for i, mix in enumerate(result.get("product_mix", []), 1):
            st.markdown(f"**{i}.** {mix}")
