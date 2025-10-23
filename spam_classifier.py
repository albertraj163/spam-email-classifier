# spam_classifier.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def main():
    df = pd.read_csv('sample_emails.csv')
    X = df['text']
    y = df['label']
    vec = TfidfVectorizer()
    Xv = vec.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(Xv, y, test_size=0.25, random_state=42)
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))

if __name__ == '__main__':
    main()
