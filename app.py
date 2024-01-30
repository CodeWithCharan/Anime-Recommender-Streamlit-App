# Import necessary libraries
import streamlit as st
import pandas as pd
# import pickle
import joblib

# load anime_dict file
# animes_dict = pickle.load(open('models/animes_dict.pkl','rb'))
animes_dict = joblib.load('models/animes_dict.joblib')

anime_df = pd.DataFrame(animes_dict) # we have converted it into a pandas dataframe

# load both tfv and sig files
# tfv = pickle.load(open('models/tfidf_vectorizer.pkl', 'rb'))
tfv = joblib.load('models/tfidf_vectorizer.joblib')

# sig = pickle.load(open('models/sigmoid_kernel.pkl', 'rb'))
sig = joblib.load('models/sigmoid_kernel.joblib')

# set recommendation indices
rec_indices = pd.Series(anime_df.index, index=anime_df["name"])

# Recommendation Function
def give_recommendation(title, sig=sig):
    # Get the index corresponding to the provided anime title
    idx = rec_indices[title]

    # Calculate pairwise similarity scores using sigmoid kernel
    sig_score = list(enumerate(sig[idx]))

    # Sort the similarity scores in descending order
    sig_score = sorted(sig_score, key=lambda x: x[1], reverse=True)

    # Keep the top 10 most similar animes (excluding itself)
    sig_score = sig_score[1:11]
    anime_indices = [i[0] for i in sig_score]

    # Create a DataFrame with the top 10 similar animes
    rec_dic = {
        "No": range(1, 11),
        "Anime Name": anime_df["name"].iloc[anime_indices].values,
        "Rating": anime_df["rating"].iloc[anime_indices].values
    }
    dataframe = pd.DataFrame(data=rec_dic)
    dataframe.set_index("No", inplace=True)

    print(f"Recommendations for {title} viewers :\n")
    return dataframe.style.set_properties(**{"background-color": "#2a9d8f", "color": "white", "border": "1.5px solid black"})

# Title
st.title('Anime Recommendation Engine')

# Search Box
selected_anime = st.selectbox(
'Which anime did you like?',
(anime_df['name'].values))

# Recommendation Button
if st.button('Recommend'):
    with st.spinner(text='In progress'):
        user_input = selected_anime
        if user_input:
            recommendations = give_recommendation(user_input)
            st.subheader(f"Top 10 Recommendations for {selected_anime}")
            st.table(recommendations)

            selected_anime_details = anime_df[anime_df['name'] == selected_anime][['name', 'genre', 'rating', 'members']]
            st.table(selected_anime_details)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Charan")