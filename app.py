from flask import Flask, request, jsonify
import pickle
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load required NLTK resources
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

# Load the saved vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Load the saved KMeans model
with open("kmeans_model.pkl", "rb") as f:
    kmeans = pickle.load(f)

# Initialize NLP tools
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = word_tokenize(text)  # Tokenize words
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatization
    return " ".join(tokens)

# Initialize Flask app
app = Flask(__name__)

# Root route to avoid 404
@app.route("/")
def home():
    return "Welcome to the AI-Powered Accident Cause Identification API! Use the /predict endpoint to make predictions."

# Prediction route
@app.route("/predict", methods=['GET',"POST"])
def predict():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Missing 'text' field in request"}), 400

    report = data["text"]
    processed_report = preprocess_text(report)
    vectorized_report = vectorizer.transform([processed_report])
    cluster = kmeans.predict(vectorized_report)[0]

    return jsonify({"Predicted Cluster": int(cluster)})

if __name__ == "__main__":
    app.run(debug=True)


