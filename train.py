import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments 

# Load dataset
df = pd.read_csv("spam.csv")

df = df[["Category", "Message"]]
df.columns = ["label", "text"]

print(df.head())
print(df["label"].value_counts())

#Convert labels to numbers
df["label"] = df["label"].map({"ham": 0, "spam": 1})

print(df.head())
print(df["label"].value_counts())

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"])  

print(f"Train set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
print("Tokenizer loaded successfully.")

#tokenize the text data
train_encodings = tokenizer(list(X_train), truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(list(X_test), truncation=True, padding=True, max_length=128)

print("Tokenization completed.")

# Create custom dataset class
class SpamDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Create data loaders
train_dataset = SpamDataset(train_encodings, y_train.tolist())
test_dataset = SpamDataset(test_encodings, y_test.tolist())

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

print("Data loaders created successfully.")

# Load pre-trained model
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)
print("Model loaded successfully.")

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=2e-5,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# Create Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train the model
trainer.train() 
print("Training completed.")

# Evaluate the model
eval_results = trainer.evaluate()
print(f"Evaluation results: {eval_results}")

# Save the model
model.save_pretrained("spam_model")
tokenizer.save_pretrained("spam_model")
print("Model and tokenizer saved successfully.")