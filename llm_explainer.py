import ollama

def explain_sms(message, prediction, confidence):
    prompt = f"""
You are a cybersecurity expert.

Message:
{message}

Prediction:
{prediction}

Confidence:
{confidence:.2f}%

Explain in simple English:
1. Why the model predicted this.
2. Suspicious words or patterns.
3. One safety tip.

Keep it under 120 words.
"""

    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]