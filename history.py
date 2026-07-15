import pandas as pd
import os
from datetime import datetime

FILE_NAME = "history.csv"


def save_history(message, prediction, confidence, risk_score, scam_type):

    data = {
        "Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Message": message,
        "Prediction": prediction,
        "Confidence": round(confidence, 2),
        "Risk Score": risk_score,
        "Scam Type": scam_type
    }

    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_csv(FILE_NAME, index=False)


def load_history():

    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)

    return pd.DataFrame()