# -*- coding: utf-8 -*-

import pandas as pd
from sklearn import preprocessing
from pandas import get_dummies
from sklearn.cluster import KMeans
from sklearn import metrics

#import matplotlib.pyplot as plt

def clean( data , selected_columns , selected_columns_data):
    data = data[selected_columns]
    data = data.drop_duplicates()
    data = data.dropna()
    data.index.name = 'film_id'
    data = data.reset_index()
    info = data
    data_ = data[selected_columns_data].copy()
    return info, data_
def getRecommendation_(info, distanceMatrix, film_id):
    def getRecommendation( index_bis , info, distanceMatrix ):
        nsmallest_list = distanceMatrix.nsmallest(5, index_bis).index.values
        res = info.iloc[nsmallest_list]
        return res
    index = info.index[info['film_id'] == film_id].tolist()
    if len(index) == 0:
        return None, None
    else:
        index_ = index[0]
        selectedMovie = info.iloc[[index_]]
        recommendations = getRecommendation(index_,info,distanceMatrix)
        return selectedMovie , recommendations
def distance_matrix_( data_ ):
    def addColumnForEachGenre( data ):
        def getGenres( data ):
            serie = data.genres.str.split('|')
            serie_ = serie.agg(['sum'])
            return list(set(serie_.values[0]))
        def add_column_eachGenre( data, genres ):
            for genre in genres:
                data.loc[:,genre] = 0
            return data
        def add_column_genresSplit( data ):
            genre_plit = data['genres'].apply(split_)
            data.loc[:,'genres_split'] = genre_plit
            return data
        def fill_column_eachGenre( row ):
            genres = row.genres_split
            for genre in genres:
                row[genre] = 1
            return row
        def split( string , separator):
            return string.split(separator)
        def split_( string):
            return split(string,'|')
        data_ = add_column_eachGenre(data,getGenres(data))
        data_ = add_column_genresSplit(data)
        data_ = data_.apply(fill_column_eachGenre, axis = 1)
        data_ = data_.drop(['genres_split','genres'], axis=1)
        return data_
    def addColumnForEachDirector( data ):
        data_ = get_dummies(data['director_name'])
        data_ = pd.concat([data, data_], axis=1)
        data_ = data_.drop(['director_name'], axis=1)
        return data_;
    def distance_matrix( data ):
        dist_ = metrics.pairwise.euclidean_distances(data)
        dist_ = pd.DataFrame(dist_)
        return dist_
    data_ = addColumnForEachGenre(data_)
    data_ = addColumnForEachDirector(data_)
    data_ = preprocessing.scale(data_, with_mean=False )
    return distance_matrix(data_)

def init():
    data = pd.read_csv('data.csv', sep=",")
    global movies
    global distanceMatrix
    selected_columns_data = ['genres','duration','gross','director_name','budget','title_year']
    selected_columns =  ['movie_title'] + selected_columns_data
    movies, data_ = clean( data , selected_columns , selected_columns_data)
    distanceMatrix = distance_matrix_(data_)
    return
def getRecommendation(film_id ):
    selectedMovie, recommendations = getRecommendation_(movies,distanceMatrix,film_id)
    return getRecommendation_display(selectedMovie,recommendations  )
def getRecommendation_display(selectedMovie,recommendations ):
    if movie is None or recommendations is None:
        return 'Recommendation not available for this movie'
    else:
        selectedMovie_ = selectedMovie[['movie_title','film_id']].to_string(index=False,header=False)
        recommendations_ = recommendations[['movie_title','film_id']].to_string(index=False,header=False)
        return selectedMovie_ + '------------' + recommendations_
