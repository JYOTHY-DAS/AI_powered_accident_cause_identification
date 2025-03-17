# AI-Powered Accident Cause Identification

## Overview
This repository contains two separate projects for **accident cause identification**:
1. **Traditional NLP Approach**: Uses **TF-IDF vectorization** and **Random Forest (with GridSearchCV) classification**.
2. **LLM-Based Approach**: Implements **BERT-based text classification** to predict primary and secondary accident causes.

Both methods aim to extract accident causes, risk factors, and related insights from textual accident reports. The project helps improve the accuracy and efficiency of accident data analysis.

## Features
- **Traditional NLP Approach**:
  - Data preprocessing using tokenization, stopword removal, stemming, and TF-IDF vectorization.
  - Uses **Random Forest with GridSearchCV** for classification.
  - **Used Postman to check the REST API**
  - **Gradio Chatbot** for user-friendly accident cause identification.
- **LLM-Based Approach**:
  - Fine-tuned **BERT model** for text classification.
  - **Streamlit Chatbot** for user-friendly accident cause identification.
- **Flask API** for deploying both models separately.


## Methodologies
### 1️⃣ Traditional NLP Approach
- **Data Preprocessing**: Tokenization, stopword removal, stemming, and TF-IDF feature extraction.
- **TF-IDF Vectorization**: Converts text into numerical feature vectors.
- **Random Forest (RF) with GridSearchCV**: Optimized hyperparameter tuning for accident cause classification.

### 2️⃣ LLM-Based Approach (BERT)
- **Fine-tuned BERT model** on accident datasets to extract primary and secondary causes.
- **Text Classification**: Predicts the category of an accident based on textual descriptions.
## Installation
### Clone the repository:
```bash
git clone https://github.com/JYOTHY-DAS/AI_powered_accident_cause_identification.git
cd AI_powered_accident_cause_identification
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run Flask API for Traditional NLP:
```bash
cd traditional_nlp
python app.py
```

### Run Flask API for LLM-based Model:
```bash
cd llm_based
python app.py
```

### Run Gradio Chatbot:
```bash
cd llm_based
python chatbot.py
```

## Contributors
- **Jyothy Das** ([@JYOTHY-DAS](https://github.com/JYOTHY-DAS))
- **Jemima IV** ([@JEMIMA-IV](https://github.com/Jemima-IV))
- **Meenu PV** ([@MEENU-PV](https://github.com/MEENU-PV))

## License
This project is licensed under the MIT License.

---
Feel free to contribute or raise issues!

