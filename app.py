import streamlit as st
import json
import sentiment_analysis as sa
import matplotlib.pyplot as plt

st.set_page_config(page_title="Earnings Call Analysis Dashboard", layout="wide")
st.title("📞 AI-Powered Earnings Call Insights (NotebookLM Style)")

uploaded = st.file_uploader("Upload a `.txt` transcript", type=["txt"])

if uploaded:
    transcript = uploaded.read().decode("utf-8")
    with st.spinner("Analyzing transcript using GPT-4..."):
        raw = sa.analyze_sentiment(transcript)
        result = json.loads(raw)

    # Company Overview
    st.subheader("🏢 Company Overview")
    c1, c2 = st.columns(2)
    c1.metric("Company", result.get("company_name", "N/A"))
    c2.metric("Sector", result.get("sector_name", "N/A"))

    st.markdown("---")

    # Tabs Layout for Insights
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
            color = "🟢" if sentiment == "Optimistic" else "🟡" if "Neutral" in sentiment else "🔴"
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
