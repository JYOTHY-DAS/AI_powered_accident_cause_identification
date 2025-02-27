from flask import Flask, request, jsonify
import joblib
import re
import spacy
from nltk.corpus import stopwords

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load trained models
model_primary = joblib.load('accident_model_primary.pkl')
model_secondary = joblib.load('accident_model_secondary.pkl')
model_risk = joblib.load('accident_model_risk.pkl')

# Load encoders
label_encoder_primary = joblib.load('label_encoder_primary.pkl')
label_encoder_secondary = joblib.load('label_encoder_secondary.pkl')
label_encoder_risk = joblib.load('label_encoder_risk.pkl')

# Load vectorizer
vectorizer = joblib.load('vectorizer.pkl')

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    doc = nlp(text)
    words = [token.lemma_.lower() for token in doc if token.text.lower() not in stopwords.words('english')]
    return " ".join(words)

# Prediction function
def predict_causes(report):
    processed_text = preprocess_text(report)
    vectorized_text = vectorizer.transform([processed_text])

    # Predict using models
    primary_cause = label_encoder_primary.inverse_transform(model_primary.predict(vectorized_text))[0]
    secondary_cause = label_encoder_secondary.inverse_transform(model_secondary.predict(vectorized_text))[0]
    risk_factor = label_encoder_risk.inverse_transform(model_risk.predict(vectorized_text))[0]

    return {
        "Primary Cause": primary_cause,
        "Secondary Cause": secondary_cause,
        "Risk Factor": risk_factor
    }

# Flask API
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "Please provide an accident report text"}), 400

    response = predict_causes(data['text'])
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
