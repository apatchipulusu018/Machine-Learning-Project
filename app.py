import streamlit as st
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Setup
nltk.download('vader_lexicon')
vader = SentimentIntensityAnalyzer()
model_name = "BAAI/bge-large-en-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
df = pd.read_csv("merged_spotify_dataset.csv")

# Precompute song sentiment vectors
song_vectors = df[["Compound", "Negative", "Neutral", "Positive"]].values

# App layout
st.markdown("<h1 style='color:#1DB954;'>🎵 Mood-Based Spotify Recommender</h1>", unsafe_allow_html=True)
user_input = st.text_input("Describe the music you're in the mood for:")

if user_input:
    scores = vader.polarity_scores(user_input)
    user_vec = np.array([[scores["compound"], scores["neg"], scores["neu"], scores["pos"]]])
    sims = cosine_similarity(user_vec, song_vectors)[0]
    top_indices = np.argsort(sims)[::-1][:10]
    top_songs = df.iloc[top_indices]

    st.markdown("### 🎧 Top 10 Recommended Songs")
    for _, row in top_songs.iterrows():
        st.markdown(f"""
        <div style='background-color:#191414; padding:10px; border-radius:6px; margin-bottom:10px; color:white'>
            <strong>{row['Song']}</strong><br>
            <i>{row['Artist']}</i> — <span style='color:#1DB954'>Valence: {row['valence']:.2f}</span><br>
            <small>Album: {row['album_name']}</small>
        </div>
        """, unsafe_allow_html=True)
