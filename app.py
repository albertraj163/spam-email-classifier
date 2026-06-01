import os

from flask import Flask, jsonify, render_template, request

from model import predict_email, train_model

app = Flask(__name__)

model_stats = train_model()


@app.route("/")
def index():
    return render_template("index.html", stats=model_stats)


@app.route("/api/classify", methods=["POST"])
def classify():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please enter email content to classify."}), 400

    if len(text) > 5000:
        return jsonify({"error": "Email content must be under 5000 characters."}), 400

    result = predict_email(text)
    return jsonify(result)


@app.route("/api/stats")
def stats():
    return jsonify(model_stats)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    url = f"http://127.0.0.1:{port}"
    print(f"\n  Spam Email Classifier running at {url}\n")
    app.run(host="127.0.0.1", port=port, debug=False)
