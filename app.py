import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances

# --- Load all necessary assets ---
df = pd.read_csv("processed_songs.csv")  # Your cleaned, final song dataset
X_embeddings = np.load("X_embeddings.npy")  # Embeddings for all tracks
regressor = joblib.load("regressor.pkl")  # Trained Ridge regression model
kmeans = joblib.load("kmeans.pkl")        # Trained KMeans model

# --- Set up the sentence embedding model ---
embedder = SentenceTransformer("BAAI/bge-large-en-v1.5")

# --- Feature columns from the training phase ---
feature_cols = [
    'Compound', 'Negative', 'Neutral', 'Positive', 'danceability', 'energy', 'key',
    'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo'
]

# --- Streamlit UI ---
st.markdown("<h1 style='color:#1DB954;'>🎵 Mood-Based Spotify Recommender</h1>", unsafe_allow_html=True)
user_input = st.text_input("Describe the kind of music you're in the mood for:")

if user_input:
    # Step 1: Embed user query
    user_embedding = embedder.encode([user_input], convert_to_numpy=True, normalize_embeddings=True)

    # Step 2: Predict Spotify features from query
    predicted_features = regressor.predict(user_embedding)[0]

    # Step 3: Assign query to a cluster
    user_cluster = kmeans.predict(user_embedding)[0]
    cluster_indices = np.where(kmeans.labels_ == user_cluster)[0]

    # Step 4: Find closest tracks in that cluster
    distances = cosine_distances(user_embedding, X_embeddings[cluster_indices])[0]
    nearest_indices = cluster_indices[np.argsort(distances)[:10]]
    recommendations = df.iloc[nearest_indices]

    # Step 5: Display top 10 recommendations
    st.markdown("### 🎧 Top 10 Recommended Songs")
    for _, row in recommendations.iterrows():
        st.markdown(f"""
        <div style='background-color:#191414; padding:10px; border-radius:6px; margin-bottom:10px; color:white'>
            <strong>{row['Song']}</strong><br>
            <i>{row['Artist']}</i> — <span style='color:#1DB954'>Valence: {row['valence']:.2f}</span><br>
            <small>Genre: {row['track_genre']}, Album: {row['album_name']}</small>
        </div>
        """, unsafe_allow_html=True)