import sys
import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from umap import UMAP
import hdbscan
from sklearn.feature_extraction.text import CountVectorizer

filepath = sys.argv[1]
df = pd.read_csv(filepath)


def run_bert(n_neighbors, n_components, min_cluster_size):
  reviews = df['review'].tolist()

  # Define UMAP model
  umap_model = UMAP(n_neighbors=n_neighbors, 
                    n_components=n_components, 
                    min_dist=0.0, 
                    metric='cosine', 
                    random_state=17)

  # Define HDBSCAN model
  hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size,
                                  metric='euclidean',
                                  cluster_selection_method='leaf',
                                  prediction_data=True)

  # Optional: define your own CountVectorizer (you can customize stop_words, ngram_range etc.)
  vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english")

  # Initialize BERTopic with custom components
  topic_model = BERTopic(umap_model=umap_model,
                        hdbscan_model=hdbscan_model,
                        vectorizer_model=vectorizer_model,
                        calculate_probabilities=True,
                        nr_topics="auto")

  # Fit the model
  topics, probs = topic_model.fit_transform(reviews)

  # Add topic IDs and topic names to DataFrame
  df["topic_id"] = topics

  topic_info = topic_model.get_topic_info()
  topic_names = {}
  for topic_id in topic_info.Topic:
      if topic_id != -1:
          words = ", ".join([word for word, _ in topic_model.get_topic(topic_id)])
          topic_names[topic_id] = words
      else:
          topic_names[topic_id] = "Outlier"

  df["topic_name"] = df["topic_id"].map(topic_names)


res = []
done = 0

# n_neighbors, n_components, min_cluster_size
for i in range(5, 21):
  for j in range(5, 21):
    for k in range(5, 40, 5):
      run_bert(i, j, k)

      unique = len(df["topic_name"].unique())
      outlier = len(df[df["topic_name"] == "Outlier"])

      res.append({
          "n_neighbors": i,
          "n_components": j,
          "min_cluster_size": k,
          "unique": unique,
          "outlier": outlier
      })

      done += 1
      print(f"Done: {done}")

res_df = pd.DataFrame(res)
res_df.to_csv("experiment_bert.csv", index=False)