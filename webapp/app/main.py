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
    """ data.shape
    (5043, 7)
    (4920, 7)
    (3789, 7)
    """
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
def display(movie, recommendations ):
    def print_( string ):
        separator = "---------------------------"
        print(separator + " " + string + " " + separator)
        return
    if movie is None or recommendations is None:
        print_('Recommendation not available for ' + film_id)
    else:
        selected_columns_display = ['movie_title', 'genres','director_name','title_year']
        print_("Selected Movie:")
        print(movie[selected_columns_display].to_string(index=False,header=False))
        print_("Recommendations:")
        print(recommendations[selected_columns_display].to_string(index=False,header=False))
def recommendations(movies , data_):
    film_ids = [3,9,283,631,2607] # 3 The Dark Knight Rises - 9 Harry Potter - 283 Gladiator - 631 Twillight - 2607 The King's Speech
    for film_id in film_ids:
        selectedMovie, recommendations = getRecommendation_(movies,distanceMatrix,film_id)
        display(selectedMovie, recommendations )
    return

def clustering_process( data_ ):
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
    data_ = addColumnForEachGenre(data_)
    data_ = addColumnForEachDirector(data_)
    data_ = preprocessing.scale(data_, with_mean=False )
    return data_

def clustering_plotSilhouette( data_ ):
    start = 100
    end = 1100
    #end = 1100
    range_ = [2] + range(start, end, 100)
    res =[]
    for k in range_:
        kmeans = KMeans(n_clusters=k).fit(data_)
        res.append(metrics.silhouette_score(data_,kmeans.labels_))
    plt.plot(range_,res,marker='o')
    plt.xlabel('Score de Silhouette')
    plt.savefig('scoreSilhouette_{}_{}.png'.format(start,end))
    plt.show()
    return
def init():
    data = pd.read_csv('data.csv', sep=",")
    global movies
    global distanceMatrix
    selected_columns_data = ['genres','duration','gross','director_name','budget','title_year']
    selected_columns = selected_columns_data + ['movie_title']
    movies, data_ = clean( data , selected_columns , selected_columns_data)
    distanceMatrix = distance_matrix_(data_)
    return
def getRecommendation(film_id ):
    selectedMovie, recommendations = getRecommendation_(movies,distanceMatrix,film_id)
    return getRecommendation_display(selectedMovie,recommendations  )
def getRecommendation_display(selectedMovie,recommendations ):
    selectedMovie_ = selectedMovie.to_string(index=False,header=False)
    recommendations_ = recommendations.to_string(index=False,header=False)
    return selectedMovie_ + '<div>' + recommendations_ '</div>'
