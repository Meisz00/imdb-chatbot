import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv('final_predictions.csv')

# Ambil list genre unik
genre_set = set()
for g in df['Genre'].dropna():
    genres = [x.strip() for x in g.split(',')]
    genre_set.update(genres)
genre_list = sorted(list(genre_set))

st.title("🎬 Movie Recommendation Chatbot")

st.write("Masukkan kriteria film yang kamu cari:")

# Multiselect genre
selected_genres = st.multiselect(
    "Pilih genre:",
    options=genre_list,
    default=[]
)

min_rating = st.slider("Minimal Rating:", 0.0, 10.0, 7.0)
keyword = st.text_input("Kata kunci bahasa inggris dalam review (opsional):", "")
sentiment = st.selectbox("Sentimen review:", ["Any", "Positive", "Negative"])
top_n = st.slider("Jumlah rekomendasi ditampilkan:", 1, 20, 5)

if st.button("Cari Rekomendasi"):
    filtered_df = df.copy()

    # Filter genre
    if selected_genres:
        genre_pattern = '|'.join(selected_genres)
        filtered_df = filtered_df[filtered_df['Genre'].str.contains(genre_pattern, case=False, na=False)]
    
    # Filter rating
    if min_rating:
        filtered_df = filtered_df[filtered_df['Rating'] >= min_rating]
    
    # Filter keyword
    if keyword:
        filtered_df = filtered_df[filtered_df['Review'].str.contains(keyword, case=False, na=False)]
    
    # Filter sentiment
    if sentiment != "Any":
        filtered_df = filtered_df[filtered_df['PredictedSentiment'] == sentiment]
    
    if filtered_df.empty:
        st.warning("Tidak ditemukan film sesuai kriteria.")
    else:
        filtered_df = filtered_df.sort_values(by='Rating', ascending=False)
        st.write(filtered_df[['Title', 'Genre', 'Rating', 'PredictedSentiment', 'Review']].head(top_n))
