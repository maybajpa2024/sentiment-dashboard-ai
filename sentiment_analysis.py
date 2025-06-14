import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_sentiment(transcript_text: str) -> dict:
    prompt = f"""
You are a senior equity research analyst. Carefully analyze the following con-call transcript.

Return the following JSON object:

{{
  "company_name": "...",
  "sector_name": "...",
  "overall_sentiment": "...",
  "sentiment_breakdown": {{
    "positive": ...,
    "neutral": ...,
    "negative": ...
  }},
  "highlights": [
    {{"quote": "...", "sentiment": "..."}}
  ],
  "key_takeaways": ["..."],
  "industry_trends": ["..."],
  "product_mix": ["..."]
}}

Use concrete bullet‐points for takeaways, trends & product mix. Include clear numeric % breakdown.

Transcript:
{transcript_text}
"""
    resp = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content
