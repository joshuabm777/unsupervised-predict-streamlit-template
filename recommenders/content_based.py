"""

    Content-based filtering for item recommendation.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: You are required to extend this baseline algorithm to enable more
    efficient and accurate computation of recommendations.

    !! You must not change the name and signature (arguments) of the
    prediction function, `content_model` !!

    You must however change its contents (i.e. add your own content-based
    filtering algorithm), as well as altering/adding any other functions
    as part of your improvement.

    ---------------------------------------------------------------------

    Description: Provided within this file is a baseline content-based
    filtering algorithm for rating predictions on Movie data.

"""

# Script dependencies
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Importing data
movies = pd.read_csv('resources/data/movies.csv', sep = ',')
ratings = pd.read_csv('resources/data/ratings.csv')
imdb = pd.read_csv('resources/data/imdb_data.csv')
movies.dropna(inplace=True)

def data_preprocessing(subset_size):
    """Prepare data for use within Content filtering algorithm.

    Parameters
    ----------
    subset_size : int
        Number of movies to use within the algorithm.

    Returns
    -------
    Pandas Dataframe
        Subset of movies selected for content-based filtering.

    """
    df = pd.merge(movies,imdb, on = 'movieId', how = 'left')
    df.drop(columns=['runtime', 'budget'], axis=1, inplace=True)

        #Ensure all datatypes are strings

    cols = ['title_cast', 'plot_keywords', 'genres', 'director']
    for col in cols:
        df[col] = df[col].astype(str)

        #Concatenate the names in the director and title_cast columns

    df.director = df.director.apply(lambda name: "".join(name.lower() for name in name.split()))
    df.title_cast = df.title_cast.apply(lambda name: "".join(name.lower() for name in name.split()))

        #Clean the rows of any special characters (|) and then fix the title cast column

    df.title_cast = df.title_cast.map(lambda x: x.split('|')[:5])
    df.title_cast = df.title_cast.apply(lambda x: " ".join(x))

        #Clean the plot keywords the same way, retrieving the first five words again

    df.plot_keywords= df.plot_keywords.map(lambda keyword: keyword.split('|')[:5])
    df.plot_keywords = df.plot_keywords.apply(lambda keyword: " ".join(keyword))

        #Cleaning the genres column

    df.genres = df.genres.map(lambda word: word.lower().split('|'))
    df.genres = df.genres.apply(lambda word: " ".join(word))

        #Merge the columns for our vectorizer

    df['word_bank'] = ''
    word_bank = []

    cols = ['title_cast', 'director', 'plot_keywords', 'genres']

        #Generate the word_bank: ie. a list of words to feed into the vectorizer

    for row in range(len(df)):
        string_ = ''
        for col in cols:
            string_ += df.iloc[row][col] + " "        
        word_bank.append(string_)

        #Append wordbank list as a column to dataframe

    df['word_bank'] = word_bank

        #Drop the columns

    df.drop(columns=['title_cast', 'director', 'plot_keywords', 'genres'], inplace=True)

    #return df
    
    #pre_processed_df = word_bank_maker()
    
    # Split genre data into individual words.
    #movies['keyWords'] = movies['genres'].str.replace('|', ' ')
    # Subset of the data
    movies_subset = df[:subset_size]
    return movies_subset

# !! DO NOT CHANGE THIS FUNCTION SIGNATURE !!
# You are, however, encouraged to change its content.  
def content_model(movie_list,top_n=10):
    """Performs Content filtering based upon a list of movies supplied
       by the app user.

    Parameters
    ----------
    movie_list : list (str)
        Favorite movies chosen by the app user.
    top_n : type
        Number of top recommendations to return to the user.

    Returns
    -------
    list (str)
        Titles of the top-n movie recommendations to the user.

    """
    # Initializing the empty list of recommended movies
    recommended_movies = []
    data = data_preprocessing(27000)
    # Instantiating and generating the count matrix
    count_vec = CountVectorizer()
    count_matrix = count_vec.fit_transform(data['word_bank'])
    indices = pd.Series(data['title'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    # Getting the index of the movie that matches the title
    idx_1 = indices[indices == movie_list[0]].index[0]
    idx_2 = indices[indices == movie_list[1]].index[0]
    idx_3 = indices[indices == movie_list[2]].index[0]
    # Creating a Series with the similarity scores in descending order
    rank_1 = cosine_sim[idx_1]
    rank_2 = cosine_sim[idx_2]
    rank_3 = cosine_sim[idx_3]
    # Calculating the scores
    score_series_1 = pd.Series(rank_1).sort_values(ascending = False)
    score_series_2 = pd.Series(rank_2).sort_values(ascending = False)
    score_series_3 = pd.Series(rank_3).sort_values(ascending = False)
    # Getting the indexes of the 10 most similar movies
    listings = score_series_1.append(score_series_1).append(score_series_3).sort_values(ascending = False)

    # Store movie names
    recommended_movies = []
    # Appending the names of movies
    top_50_indexes = list(listings.iloc[1:50].index)
    # Removing chosen movies
    top_indexes = np.setdiff1d(top_50_indexes,[idx_1,idx_2,idx_3])
    for i in top_indexes[:top_n]:
        recommended_movies.append(list(movies['title'])[i])
    return recommended_movies
