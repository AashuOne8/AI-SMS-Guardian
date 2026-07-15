import pandas as pd

def get_statistics(history):

    total = len(history)

    if total == 0:
        return {
            "total": 0,
            "spam": 0,
            "safe": 0,
            "avg_confidence": 0,
            "avg_risk": 0,
            "highest_risk": 0
        }

    spam = len(history[history["Prediction"] == "Spam"])
    safe = len(history[history["Prediction"] == "Safe"])

    return {
        "total": total,
        "spam": spam,
        "safe": safe,
        "avg_confidence": history["Confidence"].mean(),
        "avg_risk": history["Risk Score"].mean(),
        "highest_risk": history["Risk Score"].max()
    }