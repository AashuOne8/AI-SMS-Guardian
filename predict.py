import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Load trained model
model = AutoModelForSequenceClassification.from_pretrained(
    "results/checkpoint-837"
)

model.eval()

print("Model loaded successfully!")

#Enter a message
text = input("Enter your message : ")

# Tokenize the input text
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)

# Make prediction
with torch.no_grad():
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1)

# Print the prediction
if prediction == 1:
    print("The message is classified as SPAM.")
else:
    print("The message is classified as NOT SPAM.")