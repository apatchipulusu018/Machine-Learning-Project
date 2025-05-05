import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge


df = pd.read_csv("merged_spotify_dataset.csv")

device = "cuda" if torch.cuda.is_available() else "cpu"
#loading pre trained sentence embedding model here. this converts english text to vectors.
embedder = SentenceTransformer("BAAI/bge-large-en-v1.5", device=device)
regressor = Ridge()

#build text descriptions for each track. 
#the embedding model only takes in text, so we translate the charactersitics of evrey to a short english sentence.
# note: may need to tweak this description a bit
def row_to_description(row):
    return (f"A {row['track_genre']} song called '{row['Song']}' by {row['Artist']} "
            f"that is {'explicit' if row['explicit'] else 'not explicit'}, "
            f"with popularity {row['popularity']:.0f}, "
            f"{'high' if row['energy']>0.6 else 'low'} energy, "
            f"and {'high' if row['acousticness']>0.6 else 'low'} acousticness.")

descriptions = df.apply(row_to_description, axis=1).tolist()

#takes in those short english sentences for every song and computes feature vector
X_embeddings = embedder.encode(
    descriptions,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

#kmeans on embeddings
optimal_k = 5
kmeans = KMeans(n_clusters=optimal_k, random_state=42).fit(X_embeddings)


def process_user_query(query_text: str, k: int = 10) -> pd.DataFrame:
    """
    1) Embed the free-text query.
    2) Assign it to a KMeans cluster.
    3) Compute distances to tracks in the same cluster.
    4) Return the top-k Song, Artist, and valence columns.
    """
    #for each user input query it translates it to a 768-vector in the same space as the songs
    q_emb = embedder.encode(
        [query_text],
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    cluster_label = kmeans.predict(q_emb)[0]
    cluster_idxs  = np.where(kmeans.labels_ == cluster_label)[0]
    distances = np.linalg.norm(X_embeddings[cluster_idxs] - q_emb, axis=1)
    nearest_idxs = cluster_idxs[np.argsort(distances)[:10]]
    songs   = df.loc[nearest_idxs, 'Song'].tolist()
    artists = df.loc[nearest_idxs, 'Artist'].tolist()
    return list(zip(songs, artists))

