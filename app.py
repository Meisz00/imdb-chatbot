import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('final_predictions.csv')

st.title("🎬 Movie Recommendation Chatbot")

st.write("Masukkan kriteria film yang kamu cari:")

# Input user
genre = st.text_input("Genre (misalnya: Comedy, Drama):", "")
min_rating = st.slider("Minimal Rating:", 0.0, 10.0, 7.0)
keyword = st.text_input("Kata kunci dalam review (opsional):", "")
sentiment = st.selectbox("Sentimen review:", ["Any", "Positive", "Negative"])
top_n = st.slider("Berapa rekomendasi ditampilkan:", 1, 20, 5)

if st.button("Cari Rekomendasi"):
    filtered_df = df.copy()

    if genre:
        filtered_df = filtered_df[filtered_df['Genre'].str.contains(genre, case=False, na=False)]
    if min_rating:
        filtered_df = filtered_df[filtered_df['Rating'] >= min_rating]
    if keyword:
        filtered_df = filtered_df[filtered_df['Review'].str.contains(keyword, case=False, na=False)]
    if sentiment != "Any":
        filtered_df = filtered_df[filtered_df['PredictedSentiment'] == sentiment]

    if filtered_df.empty:
        st.warning("Tidak ditemukan film sesuai kriteria.")
    else:
        filtered_df = filtered_df.sort_values(by='Rating', ascending=False)
        st.write(filtered_df[['Title', 'Genre', 'Rating', 'PredictedSentiment', 'Review']].head(top_n))
