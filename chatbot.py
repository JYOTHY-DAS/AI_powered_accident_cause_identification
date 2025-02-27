import gradio as gr

def chatbot_response(report):
    cause = predict_cause(report)
    secondary = "Helmet Violation" if "helmet" in report.lower() else "Unknown"
    risk = "High" if "NH" in report or "PM" in report else "Medium"

    return f"**Primary Cause:** {cause}\n**Secondary Cause:** {secondary}\n**Risk Factor:** {risk}"

iface = gr.Interface(fn=chatbot_response, inputs="text", outputs="text")
iface.launch()
