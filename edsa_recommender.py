"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import streamlit.components.v1 as components  # html extensions
# st.set_page.config(layout='wide', initial_sidebar_state='expanded')
import streamlit_option_menu
from streamlit_option_menu import option_menu
import base64

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
ratings = pd.read_csv('resources/data/ratings.csv')
movies = pd.read_csv('resources/data/movies.csv')

# App declaration
def main():
    # st.sidebar.markdown('side')
    st.markdown(
        """
        <style>
        .reportview-container {
        background: url('resources/imgs/sample.jpg')
        }
        .sidebar .sidebar-content {
        background: url('resources/imgs/sample.jpg')
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    with st.sidebar:
        st.write('**Bene Movie Recommender App**')
        from PIL import Image

        page_selection = option_menu(
            menu_title=None,
            options=["Recommender System", "Movie Information", "EDA", "Solution Overview"],
            menu_icon='cast',
            default_index=0,

        )
    # page_options = ["Recommender System","Movie Facts","Exploratory Data Analysis","About"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    # page_selection = st.sidebar.radio("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png', use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('First Choice', title_list[14930:15200])
        movie_2 = st.selectbox('Second Choice', title_list[25055:25255])
        movie_3 = st.selectbox('Third Choice', title_list[21100:21200])
        fav_movies = [movie_1, movie_2, movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i + 1) + '. ' + j)
                except Exception as e:
                    st.write(e)
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")

        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i + 1) + '. ' + j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")

    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Movie Information":
        # Header Contents
        st.write("# Movie Information")
        images = ['resources/imgs/info.png']
        for i in images:
            st.image(i, use_column_width=True)
        filters = ["Top rated Movies", "High Budget Movies"]
        filter_selection = st.selectbox("Fact Check", filters)
        if filter_selection == "Top rated Movies":
            movie_list = pd.read_csv('resources/data/movies.csv')
            ratings = pd.read_csv('resources/data/ratings.csv')
            df = pd.merge(movie_list, ratings, on='movieId', how='left')
            movie_ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
            movie_ratings["Number_Of_Ratings"] = pd.DataFrame(df.groupby('title')['rating'].count())
            indes = movie_ratings.index
            new_list = []
            for movie in indes:
                i = ' '.join(movie.split(' ')[-1])
                new_list.append(i)
            new_lists = []
            for i in new_list:
                if len(i) < 2:
                    empty = i
                    new_lists.append(empty)
                elif i[0] == "(" and i[-1] == ")" and len(i) == 11:
                    R_strip = i.rstrip(i[-1])
                    L_strip = R_strip.lstrip(R_strip[0])
                    spaces = ''.join(L_strip.split())
                    data_type_int = int(spaces)
                    new_lists.append(data_type_int)
                else:
                    new_lists.append(i)
            cnn = []
            for i in new_lists:
                if type(i) != int:
                    i = 0
                    cnn.append(i)
                else:
                    cnn.append(i)
            movie_ratings["Year"] = cnn

            def user_interaction(Year, n):
                list_movies = movie_ratings[movie_ratings['Year'] == Year].sort_values('Number_Of_Ratings',
                                                                                       ascending=False).index
                return list_movies[:n]

            selected_year = st.selectbox("Year released", range(1900, 2020))
            no_of_outputs = st.radio("Movies to view", (5, 10, 20, 50))
            output_list = user_interaction(selected_year, no_of_outputs)
            new_list = []
            for movie in output_list:
                updated_line = ' '.join(movie.split(' ')[:-1])
                updated_line = "+".join(updated_line.split())
                new_list.append(updated_line)
            url = "https://www.imdb.com/search/title/?title="
            movie_links = []
            for i in new_list:
                links = url + i
                movie_links.append(links)
            dict_from_list = dict(zip(output_list, movie_links))
            for items in dict_from_list:
                st.subheader(items)


    if page_selection == "EDA":
        st.title('Data Visualization Analysis')


        st.subheader("All time Porpular Movies by ratings ( Top 10)")
        st.image('resources/imgs/popmovies.png', use_column_width=True)

        st.subheader("Total movies released per year")
        st.image('resources/imgs/movperyr.png', use_column_width=True)

        st.subheader("Treemap of Movie Genres")
        st.image('resources/imgs/treemap.png', use_column_width=True)


    if page_selection == 'Solution Overview':
        # markup(page_selection)
        st.title("Solution Overview")
        st.subheader("**This is the general overview of how the predict was approached**")
        st.write("""In today’s technology driven world, recommender systems are socially and economically critical to ensure that individuals can make optimised choices surrounding the content they engage with on a daily basis. One application where this is especially true is movie recommendations; where intelligent algorithms can help viewers find great titles from tens of thousands of options.

With this context, EDSA is challenging ME to construct a recommendation algorithm based on content or collaborative filtering, capable of accurately predicting how a user will rate a movie they have not yet viewed, based on their historical preferences.

Providing an accurate and robust solution to this challenge has immense economic potential, with users of the system being personalised recommendations - generating platform affinity for the streaming services which best facilitates their audience's viewing. """)

        # You can read a markdown file from supporting resources folder

        st.subheader("Overview")
        st.write(
                """On the internet, where the number of choices is overwhelming, there is a need to filter, prioritize and efficiently deliver relevant information in order to reduce the problem of information overload, which has created a potential problem to many Internet users. Recommender systems solve this problem by searching through large volume of dynamically generated information to provide users with personalized content and services.""")
        st.write(
                """Recommender systems are information filtering systems that deal with the problem of information overload by filtering vital information fragment out of large amount of dynamically generated information according to user’s preferences, interest, or observed behaviour about item. Recommender system has the ability to predict whether a particular user would prefer an item or not based on the user’s profile.""")
        st.write(
                """Recommender systems are beneficial to both service providers and users. They reduce transaction costs of finding and selecting items in an online shopping environment. Recommendation systems have also proved to improve decision making process and quality.""")


        st.subheader("Content Filtering-Based Recommender System")
        st.write(""" The Content-Based Recommender relies on the similarity of the items being recommended. The basic idea is that if you like an item, then you will also like a “similar” item. It generally works well when it's easy to determine the context/properties of each item.
                 A content-based recommender works with data that the user provides, either explicitly movie ratings for the MovieLens dataset. Based on that data, a user profile is generated, which is then used to make suggestions to the user. As the user provides more inputs or takes actions on the recommendations, the engine becomes more and more accurate.""")
        from PIL import Image
        image2 = Image.open('resources/imgs/content.png')
        st.image(image2, caption='Build a Recommender System to recommend a movie')


        st.subheader("Data Overview")
        st.write("""This dataset consists of several million 5-star ratings obtained from users of the online MovieLens movie recommendation service. The MovieLens dataset has long been used by industry and academic researchers to improve the performance of explicitly-based recommender systems, and now you get to as well!

For this Predict, we'll be using a special version of the MovieLens dataset which has enriched with additional data, and resampled for fair evaluation purposes.""")

        st.write(
                """For the Predictions, we will be using algorithm based on content or collaborative filtering, capable of accurately predicting how a user will rate a movie they have not yet viewed, based on their historical preferences.""")

        st.subheader("Source")
        st.write(
                """The data for the MovieLens dataset is maintained by the GroupLens research group in the Department of Computer Science and Engineering at the University of Minnesota. Additional movie content data was legally scraped from IMDB""")




if __name__ == '__main__':
    main()
