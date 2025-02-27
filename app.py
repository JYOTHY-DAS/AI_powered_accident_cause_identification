from flask import Flask, request, jsonify
import joblib
import re
import spacy
from nltk.corpus import stopwords

# Load necessary components
nlp = spacy.load("en_core_web_sm")
model = joblib.load('accident_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Initialize Flask app
app = Flask(__name__)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    doc = nlp(text)
    words = [token.lemma_.lower() for token in doc if token.text.lower() not in stopwords.words('english')]
    return " ".join(words)

# Prediction function
def predict_cause(report):
    processed_text = preprocess_text(report)
    vectorized_text = vectorizer.transform([processed_text])
    primary_cause = label_encoder.inverse_transform(model.predict(vectorized_text))[0]

    # Rule-based secondary cause detection
    secondary_cause = "Helmet Violation" if "helmet" in report.lower() else "Unknown"

    # Risk factor assessment
    risk_factor = "High" if "PM" in report or "NH" in report else "Medium"

    return {
        "Primary Cause": primary_cause,
        "Secondary Cause": secondary_cause,
        "Risk Factor": risk_factor
    }

# API endpoint for chatbot
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "Please provide an accident report text"}), 400

    response = predict_cause(data['text'])
    return jsonify(response)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
