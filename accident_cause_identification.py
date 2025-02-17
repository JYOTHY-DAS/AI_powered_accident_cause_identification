import numpy as np
import pandas as pd
import seaborn as sns
import nltk
import re #Regular expressions (regex) module. Used for pattern matching, searching, and manipulating text.
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
# Downloading necessary resources
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('punkt_tab')
###################################################################################
                               # Preprocessing
###################################################################################
df = pd.read_csv('data_100row.csv')
print(df.head())
print(df.shape)
import pandas as pd

# Rename the column properly
df.columns = ["Accident_Report"]

# Remove duplicate and missing values
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Display cleaned data
print(df.shape)
####################################################################################
                                # NLP Text cleaning
####################################################################################
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

# Apply preprocessing
df["Cleaned_Report"] = df["Accident_Report"].apply(preprocess_text)

# #Save cleaned report as csv file
# df.to_csv("cleaned_report.csv", index=False)

# Display processed data
print(df.head())
###########################################################################################
                    #Topic Modeling (LDA - Unsupervised Learning)
###########################################################################################
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Convert text into a document-term matrix
vectorizer = CountVectorizer(max_features=1000, stop_words="english")
dtm = vectorizer.fit_transform(df["Cleaned_Report"])

# Train LDA model with 5 topics
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(dtm)

# Display top words per topic
words = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    top_words = [words[i] for i in topic.argsort()[-10:]]  # Top 10 words
    print(f"Topic {topic_idx + 1}: {', '.join(top_words)}")
##########################################################################################
                            # Clustering Using KMeans
##########################################################################################
from sklearn.cluster import KMeans

# Apply KMeans clustering on document-term matrix
num_clusters = 5  # Choose number of clusters
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df["Cluster"] = kmeans.fit_predict(dtm)

# Show some clustered accident reports
print(df[["Accident_Report", "Cluster"]].head(10))
##########################################################################################
                            #Visualizing Clusters Using PCA
##########################################################################################
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Reduce to 2D for visualization
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(dtm.toarray())

# Plot clusters
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=df["Cluster"], cmap="viridis")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.title("Accident Report Clusters")
plt.colorbar(label="Cluster")
plt.show()
#########################################################################################
                            #Interpret the Clusters
#########################################################################################
for cluster_num in range(5):  # Adjust based on your number of clusters
    print(f"\nCluster {cluster_num}:")
    print(df[df["Cluster"] == cluster_num]["Accident_Report"].head(5))
    
#########################################################################################
                            #Fine-Tune the Model
                    #If topics seem too broad, increase n_components in LDA.
                    #If clusters overlap, adjust n_clusters in KMeans.
#########################################################################################
# Example: Increase topics from 5 to 7
lda = LatentDirichletAllocation(n_components=7, random_state=42)
lda.fit(dtm)

#########################################################################################
                            #Extract Key Insights
#########################################################################################
cluster_counts = df["Cluster"].value_counts()
print("Accident Distribution Across Clusters:\n", cluster_counts)

#########################################################################################
                        #Generate a Report/Dashboard
#########################################################################################
sns.barplot(x=cluster_counts.index, y=cluster_counts.values)
plt.xlabel("Cluster Number")
plt.ylabel("Number of Reports")
plt.title("Accident Report Clusters Distribution")
plt.show()
#########################################################################################
                #Deploy a Simple Clustering API (Optional)
#########################################################################################
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    report = request.json["text"]
    processed_report = preprocess_text(report)
    vectorized_report = vectorizer.transform([processed_report])
    cluster = kmeans.predict(vectorized_report)[0]
    return jsonify({"Predicted Cluster": int(cluster)})

if __name__ == "__main__":
    app.run(debug=True)
########################################################################################

########################################################################################