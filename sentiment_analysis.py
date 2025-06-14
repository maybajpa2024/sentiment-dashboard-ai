import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_sentiment(transcript_text: str) -> str:
    prompt = f"""
You are a financial analyst LLM. Extract only the following JSON from the transcript below. Do not include any commentary or prefix.

Return this exact format:

{{
  "company_name": "...",
  "sector_name": "...",
  "overall_sentiment": "...",
  "sentiment_breakdown": {{
    "positive": 0,
    "neutral": 0,
    "negative": 0
  }},
  "key_quotes": [
    {{"quote": "...", "sentiment": "..."}}
  ],
  "key_takeaways": ["..."],
  "industry_trends": ["..."],
  "product_mix": ["..."]
}}

Transcript:
{transcript_text}
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
