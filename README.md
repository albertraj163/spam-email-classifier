# Spam Email Classifier

A machine learning web app that detects **spam vs ham (legitimate)** emails using **TF-IDF** feature extraction and a **Naive Bayes** classifier built with scikit-learn.

## Features

- Professional web UI for real-time email classification
- Confidence scores and probability breakdown
- Sample emails to try instantly
- REST API endpoint for programmatic use

## Project Structure

```
spam-email-classifier/
├── app.py                 # Flask web server
├── model.py               # Model training & prediction
├── spam_classifier.py     # CLI training script
├── sample_emails.csv      # Training dataset
├── templates/index.html   # Web UI
├── static/                # CSS & JavaScript
└── requirements.txt
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app (trains model on startup)
python app.py
```

Open **http://127.0.0.1:8000** in your browser.

## CLI Training

To train the model without starting the web server:

```bash
python spam_classifier.py
```

## API

**POST** `/api/classify`

```json
{
  "text": "Win a free phone now!"
}
```

Response:

```json
{
  "label": "spam",
  "confidence": 87.3,
  "probabilities": {
    "ham": 12.7,
    "spam": 87.3
  }
}
```

## Tech Stack

- Python 3
- scikit-learn (TF-IDF + Multinomial Naive Bayes)
- Flask
- pandas
