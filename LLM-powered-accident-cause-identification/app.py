import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load Model and Tokenizer
MODEL_PATH = "bert_model.pth"  # Ensure this path is correct
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=7)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Define Prediction Function
def predict_accident_details(report):
    inputs = tokenizer(report, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {key: value.to(model.device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_class = torch.argmax(outputs.logits, dim=1).item()

    # Labels
    primary_causes = ["Rash Driving", "Weather Issues", "Road Conditions", 
                      "Helmet Violation", "Seatbelt Violation", "Signal Violation", "Pedestrian Negligence"]
    secondary_causes = ["DUI-related accident", "Over speeding and reckless maneuvering", "Heavy rain, fog, or slippery roads",
                        "Potholes, construction work, or lack of signs", "Two-wheeler rider not wearing a helmet",
                        "Car passengers not wearing seatbelts", "Jumping red lights or ignoring stop signs"]
    risk_mapping = {0: "High", 1: "High", 2: "Moderate", 3: "Moderate", 4: "Moderate", 5: "High", 6: "Moderate"}

    # Get Predictions
    primary_cause = primary_causes[predicted_class] if predicted_class < len(primary_causes) else "Unknown"
    secondary_cause = secondary_causes[predicted_class] if predicted_class < len(secondary_causes) else "Unknown"
    risk_factor = risk_mapping.get(predicted_class, "Unknown")

    return primary_cause, secondary_cause, risk_factor

# Streamlit UI
st.title("🚦 Accident Cause Prediction Chatbot")
st.write("Enter an accident report below, and the chatbot will predict the primary and secondary causes, as well as the risk factor.")

# User Input
user_input = st.text_area("Enter Accident Report:", "")

if st.button("Predict"):
    if user_input:
        primary_cause, secondary_cause, risk_factor = predict_accident_details(user_input)

        st.subheader("🔍 Prediction Results")
        st.write(f"**Primary Cause:** {primary_cause}")
        st.write(f"**Secondary Cause:** {secondary_cause}")
        st.write(f"**Risk Factor:** {risk_factor}")
    else:
        st.warning("⚠️ Please enter an accident report to get a prediction.")

