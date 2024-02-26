import pickle
import requests
import streamlit as st



# opening the pickle file
with open("data.pkl", "rb") as file:
    data_df = pickle.load(file)
    movie_list = data_df['title']
    new_df = data_df

# opening the pickle file
with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

# fetch poster




def fetch_poster(movie_id):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = '827efc867e9d3eee81840e0e661306a7'

    # Make the API request
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the poster path from the data
        poster_path = data.get('poster_path')

        # Construct the full URL for the poster
        full_poster_url = 'https://image.tmdb.org/t/p/original/' + poster_path if poster_path else None

        # Check if full_poster_url is not None before formatting
        if full_poster_url is not None:
            # Print or use the full poster URL
            print("Full Poster URL:", full_poster_url)

            return full_poster_url
        else:
            # Handle the case where the poster path is not available
            print("Error: Poster path not found in the API response.")
            return None
    else:
        # If the request was not successful, print an error message
        print("Error fetching data from the API.")
        return None


#recommend movie func
def recomend_movie(vector_movie):
    movie_index = new_df[new_df['title'] == vector_movie].index[0]
    distance = similarity[movie_index]
    movie_name = []
    recomended_movie_poster = []

    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]  # it give the index with other movies

    for i in movie_list:
        movie_id = i[0]
        # fetching name of movie
        movie_name.append(new_df.iloc[i[0]].title)

        # fetch the psoter from imdb api
        # Check if poster_url is not None before using it in st.image
        if fetch_poster(movie_id) is not None:
            recomended_movie_poster.append(fetch_poster(movie_id))
        else:
            continue

    return movie_name, recomended_movie_poster


st.title("Movie Recommender System")

option = st.selectbox("Select Name of Movie", movie_list.unique())

# displaying name and poster of recommended movie
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recomend_movie(option)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if recommended_movie_posters:
            # Check if the list has at least three elements before accessing index 2
            if len(recommended_movie_posters) >= 3 and recommended_movie_posters[0]:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])
            else:
                st.text(recommended_movie_names[0])
                # st.write("No poster available for the first recommended movie.")
        else:
            st.write("No recommended movie posters available.")

    with col2:
        if recommended_movie_posters:
            # Check if the list has at least three elements before accessing index 2
            if len(recommended_movie_posters) >= 3 and recommended_movie_posters[1]:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])
            else:

                st.text(recommended_movie_names[1])
                # st.write("No poster available for the second recommended movie.")
        else:
            st.write("No recommended movie posters available.")

    with col3:
        if recommended_movie_posters:
            # Check if the list has at least three elements before accessing index 2
            if len(recommended_movie_posters) >= 3 and recommended_movie_posters[2]:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])
            else:

                st.text(recommended_movie_names[2])
                # st.write("No poster available for the second recommended movie.")
        else:
            st.write("No recommended movie posters available.")

    with col4:

        if recommended_movie_posters:
            # Check if the list has at least three elements before accessing index 2
            if len(recommended_movie_posters) >= 3 and recommended_movie_posters[3]:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])
            else:

                st.text(recommended_movie_names[3])
                # st.write("No poster available for the second recommended movie.")
        else:
            st.write("No recommended movie posters available.")

    with col5:
        if recommended_movie_posters:
            # Check if the list has at least three elements before accessing index 2
            if len(recommended_movie_posters) >= 3 and recommended_movie_posters[4]:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])
            else:

                st.text(recommended_movie_names[4])
                # st.write("No poster available for the second recommended movie.")
        else:
            st.write("No recommended movie posters available.")
