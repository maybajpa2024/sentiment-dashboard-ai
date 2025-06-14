import os
from openai import OpenAI

# Use the new OpenAI client from SDK v1.0.0+
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_sentiment(transcript_text: str) -> str:
    prompt = f"""
You are a financial analyst LLM assistant. Analyze this earnings call transcript and return structured insights in the following JSON format:

{{
  "company_name": "...",
  "sector_name": "...",
  "overall_sentiment": "...",
  "sentiment_breakdown": {{
    "positive": ...,
    "neutral": ...,
    "negative": ...
  }},
  "key_quotes": [
    {{"quote": "...", "sentiment": "..."}}
  ],
  "key_takeaways": ["..."],
  "industry_trends": ["..."],
  "product_mix": ["..."]
}}

Focus on clarity, business impact, and insightfulness. No commentary or extra output.

Transcript:
{transcript_text}
"""

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
