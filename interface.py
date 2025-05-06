import streamlit as st
import pandas as pd
from recommender import process_user_query  
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.markdown("""
    <style>
    .stApp {
        background-color:#BFC58780
;
    }
    .stApp h1 {
        text-align: center !important;
        font-size: 3rem !important;
        color: #959D56 !important;
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
        width: 100% !important;
        text-align: left !important;
        font-size: 1rem !important;
        padding-left: 40px !important; /* make room for icon */
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/5/55/Magnifying_glass_icon.svg');
        background-size: 20px 20px !important;
        background-repeat: no-repeat !important;
        background-position: 10px center !important;
    }
    </style>
""", unsafe_allow_html=True)

#Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="21d1a4900aee4e10a6a6bef521fc8bac",
    client_secret="645b670787b54403b729fff56e6435aa"
))

st.markdown("<h1 style='text-align:center; font-size:3rem; color:#959D56'>🎵 Moodify 🎵</h1>", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align:center; font-size:1.5rem; color:  #000000'>"
    "Describe the type of music you’re in the mood for:"
    "</h2>",
    unsafe_allow_html=True
)

user_input = st.text_input("", key="mood_input")


if user_input:
    top_songs = process_user_query(user_input)  # returns list of (song, artist)

    st.markdown("### Top 10 Recommended Songs:")
    for i, (song_name, artist_name) in enumerate(top_songs, start=1):
        

        try:
            results = sp.search(q=f"{song_name} {artist_name}", type="track", limit=1)
            items   = results.get("tracks", {}).get("items", [])
            if items:
                track       = items[0]
                track_url   = track["external_urls"]["spotify"]
            
                album_img   = track["album"]["images"][1]["url"]
            else:
                track_url, album_img = None, None
        except Exception:
            track_url, album_img = None, None

        img_html = (f"<img src='{album_img}' width='60' height='60' "
                    "style='border-radius:4px; margin-right:12px;' />") if album_img else ""
        play_btn = (f"<a href='{track_url}' target='_blank' style='text-decoration:none;'>"
                    "<button style="
                    "'background-color:#BFC58780;"
                    "border:none;"
                    "border-radius:4px;"
                    "padding:8px 12px;"
                    "color:white;"
                    "font-size:1rem;"
                    "cursor:pointer'"
                    ">▶️ Play</button></a>") if track_url else ""

        st.markdown(f"""
        <div style="
            display:flex;
            align-items:center;
            background-color:#959D56;
            padding:10px;
            border-radius:6px;
            margin-bottom:10px;
            color:white;
        ">
            {img_html}
            <div style="flex:1; text-align:left;">
            <strong style="font-size:1.1rem;">{i}. {song_name}</strong><br>
            <em style="opacity:0.8;">{artist_name}</em>
            </div>
            {play_btn}
        </div>
        """, unsafe_allow_html=True)
