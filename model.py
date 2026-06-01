import pickle
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

MODEL_DIR = Path(__file__).parent / "models"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"
CLASSIFIER_PATH = MODEL_DIR / "classifier.pkl"
DATA_PATH = Path(__file__).parent / "sample_emails.csv"


def train_model(data_path: Path = DATA_PATH) -> dict:
    df = pd.read_csv(data_path)
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(df["text"])
    labels = df["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.25, random_state=42
    )

    classifier = MultinomialNB()
    classifier.fit(x_train, y_train)
    predictions = classifier.predict(x_test)
    report = classification_report(y_test, predictions, output_dict=True)

    MODEL_DIR.mkdir(exist_ok=True)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(CLASSIFIER_PATH, "wb") as f:
        pickle.dump(classifier, f)

    return {
        "accuracy": round(report["accuracy"] * 100, 1),
        "samples": len(df),
        "spam_count": int((labels == "spam").sum()),
        "ham_count": int((labels == "ham").sum()),
    }


def load_model():
    if not VECTORIZER_PATH.exists() or not CLASSIFIER_PATH.exists():
        return None, None

    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(CLASSIFIER_PATH, "rb") as f:
        classifier = pickle.load(f)

    return vectorizer, classifier


def predict_email(text: str) -> dict:
    vectorizer, classifier = load_model()
    if vectorizer is None or classifier is None:
        raise RuntimeError("Model not trained. Run training first.")

    features = vectorizer.transform([text.strip()])
    label = classifier.predict(features)[0]
    probabilities = classifier.predict_proba(features)[0]
    classes = list(classifier.classes_)
    confidence = round(max(probabilities) * 100, 1)

    return {
        "label": label,
        "confidence": confidence,
        "probabilities": {
            cls: round(prob * 100, 1) for cls, prob in zip(classes, probabilities)
        },
    }
