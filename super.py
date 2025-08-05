import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import fitz
import re
import pandas as pd




# Load the dataset
df = pd.read_csv("resume_classifier_dataset.csv")

# Show the first 5 rows
#print(df.head())

# Drop 'file_name' since it's not useful for training
X = df.drop(columns=['file_name', 'label'])  # Features
y = df['label']  # Labels

#print(X.head())
#print(y.head())



# Split the data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#print("Training samples:", (X_train))
#print("Testing samples:", (X_test))



# Create the model
clf = DecisionTreeClassifier(random_state=42)

# Train the model on training data
clf.fit(X_train, y_train)



# Make predictions on test data
y_pred = clf.predict(X_test)

# Print predictions and actual values
#print("Predicted labels:", y_pred)
#print("Actual labels:   ", y_test.values)

# Evaluate the model
#print("\nAccuracy:", accuracy_score(y_test, y_pred))
#print("\nClassification Report:\n", classification_report(y_test, y_pred))
#print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))


def extract_text_from_pdf(file_path):
    text=""
    with fitz.open(file_path) as doc:
        for ans in doc:
            text+=ans.get_text()
    return text

file_path="resume/david_resume.pdf"
output=extract_text_from_pdf(file_path)

import re
import pandas as pd

# --- Helpers: regex patterns ---
EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.I)
# Phone regex: matches common international/local patterns (very permissive)
PHONE_RE = re.compile(r'(\+?\d{1,3}[\s-]?)?(\(?\d{2,4}\)?[\s-]?)?[\d\s.-]{6,15}')

# Education keywords (expand as needed)
EDU_KEYWORDS = [
    r'\bbachelor\b', r'\bb\.?tech\b', r'\bbsc\b', r'\bmsc\b', r'\bmtech\b',
    r'\bmba\b', r'\bmaster\b', r'\bphd\b', r'\bdegree\b', r'\buniversity\b',
    r'\bcollege\b', r'\bhigh school\b', r'\bdiploma\b', r'\bclass of\b'
]
EDU_RE = re.compile('|'.join(EDU_KEYWORDS), re.I)

def extract_features_from_text(text, filename="unknown"):
    # Normalize whitespace
    txt = re.sub(r'\s+', ' ', text).strip()
    
    # word count (split on whitespace)
    word_count = len(txt.split()) if txt else 0

    # has_email
    has_email = int(bool(EMAIL_RE.search(txt)))

    # has_phone
    # phone regex can return many false positives; we do a quick filter:
    

    # has_education_keywords
    has_education_keywords = int(bool(EDU_RE.search(txt)))

    return {
        "file_name": filename,
        "word_count": word_count,
        "has_email": has_email,
        "has_education_keywords": has_education_keywords
    }

# --- Use it with your extracted text variable 'output' and file_path ---

features = extract_features_from_text(output, filename=file_path)

# Prepare DataFrame row with the exact columns used in training (and order)
cols = ['file_name','word_count','has_email','has_education_keywords']
row_df = pd.DataFrame([[
    features['file_name'],
    features['word_count'],
    features['has_email'],
    features['has_education_keywords']
]], columns=cols)

# Since model was trained on numeric features only (excluding file_name),
# create X_new with same numeric columns order as training:
X_new = row_df.drop(columns=['file_name'])

print("Extracted features:")
print(row_df.to_string(index=False))

# Predict using clf (must be in memory)
pred = clf.predict(X_new)[0]   # 1 or 0

print("\nPrediction:", pred, "→", ("RESUME" if pred == 1 else "NOT A RESUME"))
