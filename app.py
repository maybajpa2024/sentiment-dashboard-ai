import streamlit as st
import json
import sentiment_analysis as sa
import matplotlib.pyplot as plt

st.set_page_config(page_title="Earnings Call Sentiment Dashboard", layout="wide")
st.title("📞 Earnings Call Insights Dashboard")

uploaded = st.file_uploader("Upload Earnings Call Transcript (.txt)", type=["txt"])
if uploaded:
    text = uploaded.read().decode("utf-8")
    raw = sa.analyze_sentiment(text)
    result = json.loads(raw)

    # Company & Sector
    st.subheader("🏢 Company Overview")
    c1, c2 = st.columns(2)
    c1.metric("Company", result.get("company_name", "—"))
    c2.metric("Sector", result.get("sector_name", "—"))

    # Sentiment Pie
    st.subheader("📊 Sentiment Breakdown")
    labels = list(result["sentiment_breakdown"].keys())
    sizes = list(result["sentiment_breakdown"].values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # Overall Tone & Highlights
    st.subheader("🧠 Overall Tone")
    st.info(result["overall_sentiment"])

    st.subheader("🗣️ Key Quotes")
    for quote in result.get("highlights", []):
        st.markdown(f"**{quote['sentiment']}**: “{quote['quote']}”")

    # Business Takeaways
    st.subheader("✅ Business Takeaways")
    for i, item in enumerate(result.get("key_takeaways", []), 1):
        st.markdown(f"**{i}.** {item}")

    # Industry Trends
    st.subheader("📈 Industry Trends")
    for i, item in enumerate(result.get("industry_trends", []), 1):
        st.markdown(f"**{i}.** {item}")

    # Product Mix Commentary
    st.subheader("🧪 Product / Segment Commentary")
    for i, item in enumerate(result.get("product_mix", []), 1):
        st.markdown(f"**{i}.** {item}")
