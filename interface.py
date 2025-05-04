import streamlit as st
import pandas as pd
from recommender import process_user_query  
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.markdown("""
    <style>
    .stApp {
        background-color: #c8e6c9;
    }
    .stApp h1 {
        text-align: center !important;
        font-size: 3rem !important;
        color: #1DB954 !important;
    }
    .stApp h2 {
        text-align: center !important;
        font-size: 1.5rem !important;
    }
    .stTextInput > div {
        display: flex !important;
        justify-content: center !important;
    }
    .stTextInput input {
        width: 60% !important;
        text-align: left !important;
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

#Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="21d1a4900aee4e10a6a6bef521fc8bac",
    client_secret="645b670787b54403b729fff56e6435aa"
))

st.markdown("<h1 style='text-align:center; font-size:3rem; color:#1DB954'>🎵 Moodify 🎵</h1>", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align:center; font-size:1.5rem;'>"
    "Describe the type of music you’re in the mood for:"
    "</h2>",
    unsafe_allow_html=True
)

user_input = st.text_input("", key="mood_input")


if user_input:
    top_songs = process_user_query(user_input, k=10)

    st.markdown("### 🎧 Top 10 Recommended Songs 🎧")
    for i, row in enumerate(top_songs.itertuples(), start=1):
        song_name   = row.Song
        artist_name = row.Artist

        st.markdown(f"""
        <div style='
            background-color:#191414;
            padding:10px;
            border-radius:6px;
            margin-bottom:10px;
            color:white;
            text-align:center;
        '>
            <strong>{i}. {song_name}</strong><br>
            <i>{artist_name}</i>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            results = sp.search(q=f"{song_name} {artist_name}", type="track", limit=1)
            items   = results.get("tracks", {}).get("items", [])
            if items:
                track_url = items[0]["external_urls"]["spotify"]
                st.markdown(f"[▶️ Listen on Spotify]({track_url})", unsafe_allow_html=True)
            else:
                st.caption("🔇 Couldn’t find on Spotify")
        except Exception:
            st.caption("🔇 Error retrieving Spotify link")
