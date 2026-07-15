import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)


def explain_sms(message, prediction, confidence):

    prompt = f"""
You are an expert cybersecurity analyst.

An AI spam detection model analyzed this SMS.

SMS:
{message}

Prediction:
{prediction}

Confidence:
{confidence:.2f}%

Explain in simple English:

1. Why the message was classified this way.
2. Mention suspicious patterns if present.
3. Mention the scam category (if any).
4. Give one safety tip.

Keep the answer under 120 words.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content