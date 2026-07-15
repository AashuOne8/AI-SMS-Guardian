from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(
    message,
    prediction,
    confidence,
    risk_level,
    risk_score,
    scam_type,
    explanation
):

    filename = "SMS_Analysis_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>AI SMS Guardian Report</b>", styles["Title"])
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(f"<b>SMS:</b> {message}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"<b>Prediction:</b> {prediction}", styles["BodyText"])
    )

    story.append(
        Paragraph(
            f"<b>Confidence:</b> {confidence:.2f}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Threat Level:</b> {risk_level}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Risk Score:</b> {risk_score}/100",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Scam Type:</b> {scam_type}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("<b>AI Explanation</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(explanation, styles["BodyText"])
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("<b>Safety Advice</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            "Do not click suspicious links. Never share OTPs or passwords. Verify the sender before taking any action.",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename