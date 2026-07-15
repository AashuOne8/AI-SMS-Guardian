import streamlit as st
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from report import create_pdf
from analytics import get_statistics
from llm_groq import explain_sms
from history import save_history, load_history
import plotly.express as px
from risk_analysis import (
    get_risk_level,
    get_risk_score,
    get_scam_type,
)

# -----------------------------
# Load Model
# -----------------------------
MODEL_NAME = "AashuOne8/ai-sms-guardian-model"

model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="🛡️ AI SMS Guardian",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AI SMS Guardian")

st.markdown("""
### Detect Spam with Explainable AI

Protect yourself from phishing, scam, and fraudulent SMS messages using a fine-tuned DistilBERT model.

---
""")

# -----------------------------
# Layout
# -----------------------------
left_col, right_col = st.columns([2, 1])

# =========================
# LEFT SIDE
# =========================
with left_col:

    st.subheader("📝 Enter SMS Message")

    message = st.text_area(
        "Type or paste your message below:",
        height=180,
        placeholder="Example: Congratulations! You won ₹50,000..."
    )

    analyze = st.button("🔍 Analyze Message")

# =========================
# RIGHT SIDE
# =========================
with right_col:

    st.subheader("🤖 AI Analysis")

    if not analyze:
        st.info("Prediction will appear here after analysis.")

# =====================================================
# Run Prediction
# =====================================================
if analyze:

    # ---------------- Prediction ----------------
    inputs = tokenizer(
        message,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    inputs.pop("token_type_ids", None)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(outputs.logits, dim=1)

    prediction = torch.argmax(probs, dim=1).item()
    confidence = probs[0][prediction].item() * 100

    # ---------------- Risk Analysis ----------------
    risk_score = get_risk_score(
        message,
        confidence,
        prediction
    )

    risk_level = get_risk_level(risk_score)
    scam_type = get_scam_type(message)

    # ---------------- AI Explanation ----------------
    explanation = explain_sms(
        message,
        "Spam" if prediction == 1 else "Safe",
        confidence
    )
    save_history(
    message,
    "Spam" if prediction == 1 else "Safe",
    confidence,
    risk_score,
    scam_type
)
    pdf_file = create_pdf(
    message,
    "Spam" if prediction == 1 else "Safe",
    confidence,
    risk_level,
    risk_score,
    scam_type,
    explanation
)

    # =====================================================
    # LEFT COLUMN
    # =====================================================
    with left_col:

        st.markdown("---")

        st.subheader("🛡️ Threat Intelligence Dashboard")

        st.markdown("### 🚨 Threat Meter")

        st.progress(risk_score / 100)

        if risk_score >= 80:
            st.error("🔴 HIGH RISK")
        elif risk_score >= 50:
            st.warning("🟠 MEDIUM RISK")
        else:
            st.success("🟢 LOW RISK")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            st.metric("🛡️ Scam Type", scam_type)
            st.metric("🎯 Confidence", f"{confidence:.2f}%")

        with c2:
            st.metric("⚠️ Risk Score", f"{risk_score}/100")
            st.metric("🚨 Threat Level", risk_level)

    # =====================================================
    # RIGHT COLUMN
    # =====================================================
    with right_col:

        if prediction == 1:
            st.error("🚨 Spam Detected")
        else:
            st.success("✅ Safe Message")

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        st.subheader("💡 AI Explanation")
        st.info(explanation)

        st.subheader("🛡️ Safety Tips")

        if prediction == 1:
            st.warning("""
• Never click unknown links.

• Never share OTP or passwords.

• Verify the sender from the official website.

• Block and report suspicious numbers.
""")
        else:
            st.success("""
• This message appears safe.

• Stay alert for unexpected requests.

• Verify any financial request before responding.
""")

        # ---------------- PDF Download ----------------
        st.subheader("📄 Download Report")

        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📥 Download PDF Report",
                data=file,
                file_name="SMS_Analysis_Report.pdf",
                mime="application/pdf"
            )
            st.divider()

st.subheader("📜 Detection History")

history = load_history()

if history.empty:
    st.info("No history available yet.")
else:
    st.dataframe(
        history.iloc[::-1],
        use_container_width=True
    )
    st.divider()
st.subheader("📊 Security Analytics")

stats = get_statistics(history)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📨 Total Messages", stats["total"])
    st.metric("🚨 Spam", stats["spam"])

with col2:
    st.metric("✅ Safe", stats["safe"])
    st.metric(
        "🎯 Avg Confidence",
        f"{stats['avg_confidence']:.2f}%"
    )

with col3:
    st.metric(
        "⚠️ Avg Risk",
        f"{stats['avg_risk']:.1f}"
    )
    st.metric(
        "🔥 Highest Risk",
        stats["highest_risk"]
    )
if not history.empty:

    st.subheader("📈 Prediction Distribution")

    fig = px.pie(
        history,
        names="Prediction",
        title="Spam vs Safe Messages",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)