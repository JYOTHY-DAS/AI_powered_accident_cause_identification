import gradio as gr
from transformers import pipeline

# Load trained model
ner_pipeline = pipeline("ner", model="bert-accident-ner", tokenizer="bert-accident-ner")

# Function to extract accident causes
def identify_causes(text):
    ner_results = ner_pipeline(text)
    
    primary_causes = []
    secondary_causes = []
    risk_factors = []

    for entity in ner_results:
        word = entity["word"].replace("##", "")
        label = entity["entity"]

        if label.endswith("PRIMARY_CAUSE"):
            primary_causes.append(word)
        elif label.endswith("SECONDARY_CAUSE"):
            secondary_causes.append(word)
        elif label.endswith("RISK_FACTOR"):
            risk_factors.append(word)

    return {
        "Primary Causes": " ".join(primary_causes),
        "Secondary Causes": " ".join(secondary_causes),
        "Risk Factors": " ".join(risk_factors)
    }

# Gradio UI
iface = gr.Interface(
    fn=identify_causes,
    inputs=gr.Textbox(lines=5, placeholder="Enter accident details..."),
    outputs="json",
    title="Accident Cause Identification Chatbot"
)

# Launch chatbot
iface.launch()
