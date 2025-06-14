import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_sentiment(transcript_text: str) -> dict:
    prompt = f"""
You are a financial analyst LLM assistant. Analyze this earnings call transcript and return structured insights in the following format:

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

Rules:
- "overall_sentiment" should be one of: Optimistic, Cautiously Optimistic, Neutral, Defensive, Pessimistic
- Focus on factual business insights (revenue, margins, growth, guidance)
- Use clear bullet points with no vague language

Transcript:
{transcript_text}
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
