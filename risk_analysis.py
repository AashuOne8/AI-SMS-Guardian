# risk_analysis.py

def get_scam_type(message):
    msg = message.lower()

    if any(word in msg for word in ["otp", "verification code", "one time password"]):
        return "OTP Fraud"

    elif any(word in msg for word in ["bank", "account", "credit card", "debit card"]):
        return "Banking Scam"

    elif any(word in msg for word in ["upi", "paytm", "phonepe", "gpay", "google pay"]):
        return "UPI Payment Scam"

    elif any(word in msg for word in ["lottery", "won", "winner", "prize", "jackpot"]):
        return "Lottery Scam"

    elif any(word in msg for word in ["click", "http", "https", "bit.ly", "tinyurl", "link"]):
        return "Phishing Attack"

    elif any(word in msg for word in ["urgent", "immediately", "limited time", "act now"]):
        return "Urgency Scam"

    elif any(word in msg for word in ["gift", "reward", "bonus", "cashback"]):
        return "Reward Scam"

    elif any(word in msg for word in ["job", "salary", "work from home"]):
        return "Job Scam"

    elif any(word in msg for word in ["loan", "emi", "credit"]):
        return "Loan Scam"

    elif any(word in msg for word in ["delivery", "courier", "parcel"]):
        return "Delivery Scam"

    else:
        return "General Message"


def get_risk_score(message, confidence, prediction):
    if prediction == 0:   # Safe
        return max(0, int(100 - confidence))

    score = int(confidence)

    msg = message.lower()

    keywords = [
        "otp","bank","account","upi","click","http","https",
        "winner","won","prize","lottery","urgent",
        "verify","reward","gift","loan","delivery"
    ]

    for word in keywords:
        if word in msg:
            score += 3

    return min(score,100)

def get_risk_level(score):
    if score >= 90:
        return "CRITICAL"
    elif score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    elif score >= 15:
        return "LOW"
    else:
        return "SAFE"