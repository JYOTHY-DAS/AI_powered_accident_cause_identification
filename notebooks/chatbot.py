import gradio as gr
import joblib
import re
import spacy
from nltk.corpus import stopwords
import numpy as np

# Load components
nlp = spacy.load("en_core_web_sm")

# Load trained models
model_primary = joblib.load('accident_model_primary.pkl')
model_secondary = joblib.load('accident_model_secondary.pkl')
model_risk = joblib.load('accident_model_risk.pkl')

# Load vectorizer
vectorizer = joblib.load('vectorizer.pkl')

# Load encoders
label_encoder_primary = joblib.load('label_encoder_primary.pkl')
label_encoder_secondary = joblib.load('label_encoder_secondary.pkl')
label_encoder_risk = joblib.load('label_encoder_risk.pkl')

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    doc = nlp(text)
    words = [token.lemma_ for token in doc if token.text.lower() not in stopwords.words('english')]
    return " ".join(words)

# Prediction function
def chatbot_response(report):
    processed_text = preprocess_text(report)
    vectorized_text = vectorizer.transform([processed_text])
    
    # Predict primary cause
    primary_cause = label_encoder_primary.inverse_transform(model_primary.predict(vectorized_text))[0]
    
    # Predict secondary cause
    secondary_cause = label_encoder_secondary.inverse_transform(model_secondary.predict(vectorized_text))[0]
    
    # Predict risk factor
    risk_factor = label_encoder_risk.inverse_transform(model_risk.predict(vectorized_text))[0]
    
    return f"**Primary Cause:** {primary_cause}\n**Secondary Cause:** {secondary_cause}\n**Risk Factor:** {risk_factor}"

# Create chatbot interface
iface = gr.Interface(fn=chatbot_response,
                     inputs="text",
                     outputs="text",
                     title="Accident Cause Identifying Chatbot")
iface.launch(share=True)

