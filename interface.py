import streamlit as st
import pandas as pd
from recommender import process_user_query  
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.markdown("""<style>
.stApp {
    background-color: rgba(191,197,135,0.5) !important;
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
    width: 100% !important;
    margin: 0 auto !important;
    box-sizing: border-box !important;
}
.stTextInput input {
    width: 100% !important;
    box-sizing: border-box !important;
    padding-left: 40px !important;
    font-size: 1rem !important;
    background: url('https://upload.wikimedia.org/wikipedia/commons/5/55/Magnifying_glass_icon.svg') 
                no-repeat 10px center !important;
    background-size: 20px 20px !important;
}
</style>""", unsafe_allow_html=True)

#Spotify API setup
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="21d1a4900aee4e10a6a6bef521fc8bac",
        client_secret="645b670787b54403b729fff56e6435aa"
    )
)

st.markdown("<h1>🎵 Moodify 🎵</h1>", unsafe_allow_html=True)
st.markdown("<h2>Describe the type of music you’re in the mood for:</h2>", unsafe_allow_html=True)

user_input = st.text_input("", key="mood_input")

if user_input:
    top_songs = process_user_query(user_input)
    st.markdown("### Top 10 Recommended Songs:")

    for i, (song_name, artist_name) in enumerate(top_songs, start=1):
        try:
            results = sp.search(q=f"{song_name} {artist_name}", type="track", limit=1)
            items = results.get("tracks", {}).get("items", [])
            if items:
                track = items[0]
                track_url = track["external_urls"]["spotify"]
                album_img = track["album"]["images"][1]["url"]
            else:
                track_url, album_img = None, None
        except Exception:
            track_url, album_img = None, None

        img_html = ""
        if album_img:
            img_html = (
                f"<img src='{album_img}' width='60' height='60' "
                "style='border-radius:4px; margin-right:12px;' />"
            )

        play_btn = ""
        if track_url:
            play_btn = (
                f"<a href='{track_url}' target='_blank' "
                "style='text-decoration:none; color:white; font-size:1.5rem; margin-left:12px;'>"
                "▶️"
                "</a>"
            )

        st.markdown(f"""<div style="
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
</div>""", unsafe_allow_html=True)
