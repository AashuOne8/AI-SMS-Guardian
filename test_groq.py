from llm_groq import explain_sms

print(
    explain_sms(
        "Congratulations! You won ₹50,000. Click here to claim.",
        "Spam",
        99.5
    )
)