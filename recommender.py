import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans

# Load merged dataset
merged_df = pd.read_csv("merged_spotify_dataset.csv")

# Build text descriptions
def row_to_description(row):
    return (f"A {row['track_genre']} song called '{row['Song']}' by {row['Artist']}, "
            f"{'explicit' if row['explicit'] else 'not explicit'}, "
            f"popularity {row['popularity']:.0f}, "
            f"{'high' if row['energy'] > 0.6 else 'low'} energy, "
            f"{'high' if row['acousticness'] > 0.6 else 'low'} acousticness.")

descriptions = merged_df.apply(row_to_description, axis=1).tolist()

# Initialize embedding model
embedder = SentenceTransformer("BAAI/bge-large-en-v1.5")
X_embeddings = embedder.encode(
    descriptions,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

# Define target feature columns
feature_cols = [
    'Compound', 'Negative', 'Neutral', 'Positive',
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo'
]
y = merged_df[feature_cols].values

# Train Ridge regression model
X_train, X_test, y_train, y_test = train_test_split(X_embeddings, y, test_size=0.2, random_state=42)
regressor = Ridge()
regressor.fit(X_train, y_train)

# Fit KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=42).fit(X_embeddings)

# Define the recommendation function
def process_user_query(query_text, k=10):
    query_emb = embedder.encode([query_text], convert_to_numpy=True, normalize_embeddings=True)
    pred_feats = regressor.predict(query_emb)[0]
    cluster_label = kmeans.predict(query_emb)[0]
    cluster_idxs = np.where(kmeans.labels_ == cluster_label)[0]
    dists = np.linalg.norm(X_embeddings[cluster_idxs] - query_emb, axis=1)
    nearest = cluster_idxs[np.argsort(dists)[:k]]
    return merged_df.iloc[nearest][['Song', 'Artist', 'valence']].reset_index(drop=True)
