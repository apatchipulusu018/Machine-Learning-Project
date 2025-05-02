import streamlit as st
import pandas as pd
from recommender import process_user_query  
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="21d1a4900aee4e10a6a6bef521fc8bac",       # <-- Replace with your actual client ID
    client_secret="645b670787b54403b729fff56e6435aa" # <-- Replace with your actual client secret
))

st.markdown("<h1 style='color:#1DB954;'>🎵 Mood-Based Spotify Recommender</h1>", unsafe_allow_html=True)
user_input = st.text_input("Describe the music you're in the mood for:")

if user_input:
    top_songs = process_user_query(user_input, k=10)

    st.markdown("### 🎧 Top 10 Recommended Songs")
    for _, row in top_songs.iterrows():
        song_name = row['Song']
        artist_name = row['Artist']
        valence = row['valence']

        # Try to get preview URL from Spotify
        preview_url = None
        try:
            query = f"track:{song_name} artist:{artist_name}"
            results = sp.search(q=query, type="track", limit=1)
            items = results.get("tracks", {}).get("items", [])
            if items:
                preview_url = items[0].get("preview_url")
        except Exception as e:
            preview_url = None

        # Display song card
        st.markdown(f"""
        <div style='background-color:#191414; padding:10px; border-radius:6px; margin-bottom:10px; color:white'>
            <strong>{song_name}</strong><br>
            <i>{artist_name}</i> — <span style='color:#1DB954'>Valence: {valence:.2f}</span>
        </div>
        """, unsafe_allow_html=True)

        # Show audio preview if available
        if preview_url:
            st.audio(preview_url, format="audio/mp3")
        else:
            st.caption("🔇 No preview available")
