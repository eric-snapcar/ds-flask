# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:20:04 2017

@author: ATruong1
"""
#%%
import pandas as pd
from sklearn import preprocessing
from pandas import get_dummies
from sklearn.cluster import KMeans
from sklearn import decomposition
#%%
def cleanAndSelect_v2(data):
    #selectionne les variables listées dans car_selected ['var1', 'var2', 'var3'],
    var_selected =['num_user_for_reviews','num_voted_users','imdb_score','duration','budget','genres']

    data_ = data[['movie_title','title_year','director_name']+var_selected]
    data_ = data_.dropna()
    data_ = data_.drop_duplicates(['movie_title','title_year'])
    data_.index.name = 'film_id'
    data_ = data_.reset_index()
    info = data_
    data_ = data_[var_selected].copy()

    df1 = info[['movie_title','film_id','genres','director_name','title_year']].head(10)
    df2 = info[['movie_title','film_id','genres','director_name','title_year']].sample(10)
    print(df1.append(df2))

    #Ajout des genres
    data_ = addColumnForEachWord(data_,'genres', 0)


    #Nouveau score qui sublime les haut score avec beaucoup de votes et pénalise les score faibles avec beaucoup de vote
    score_ = data['imdb_score'].divide(10)
    num_voter_ = (data['num_voted_users']-data['num_voted_users'].mean()).divide(data['num_voted_users'].max())
    data_['new_score'] = score_.multiply(num_voter_)
    data_ = data_.drop(['imdb_score'], axis = 1)
    return data_, info
#%%
def feat_to_drop(data, threshold):
    # renvoie une liste des variables à garder après condition de fréquence avec 'threshold'
    filtered = data.sum(axis = 0) < threshold
    return filtered.index[filtered].tolist()
def addColumnForEachWord(data,variable, threshold):
    #va créer une colonne pour chaque élément presént la colonne 'variable' (pour les listes séparées par '|')
    def getWords(data):
        # obtiends une liste de tous les genres présents dans la colonne 'Genres' (unique)
        serie = data[variable].str.split('|').dropna()
        serie_ = serie.agg(['sum'])
        return list(set(serie_.values[0]))
    def add_column_eachWord(data, words):
        # rajoute une colonne pour chaque genre de film
        for word in words:
            data[word] = 0
        return data
    def add_column_wordsSplit(data):
        word_split = data[data[variable].isnull()==False][variable].apply(split_)
        data['words_split'] = word_split
        return data
    def fill_column_eachWord(row):
        #remplis les colonnes avec des 1 et des 0 si le genre correspond au film
        if pd.isnull(row[variable]) == False:
            words = row.words_split
            for word in words:
                row[word] = 1
        return row
    def split(string , separator):
        # parse un string avec des séparateurs
        return string.split(separator)
    def split_(string):
        return split(string,'|')
    data_ = add_column_eachWord(data,getWords(data))
    data_ = add_column_wordsSplit(data)
    data_ = data_.apply(fill_column_eachWord, axis = 1)
    data_ = data_.drop(['words_split',variable], axis=1)
    data_ = data_.drop(feat_to_drop(data_[getWords(data)], threshold), axis = 1)
    return data_
def addColumnForEachContent(data,variable, threshold):
    # renvoie une colonne pour chque élément dans la colonne 'variable'
    data_sup = get_dummies(data[variable])
    data_ = pd.concat([data, data_sup], axis=1)
    data_ = data_.drop(variable, axis=1)
    data_ = data_.drop(feat_to_drop(data_sup, threshold), axis=1)
    return data_
def recommend_clustering(data, info,film_id):
    index = info.index[info['film_id'] == film_id].tolist()
    if len(index) == 0:
        return None, None
    else:
        index_ = index[0]
        movie = info.iloc[[index_]]
        cluster = movie['cluster'].iloc[0]
        size_cluster = data[data['cluster']==cluster].shape[0]
        if size_cluster < 5:
            lis_index = data[data['cluster']==cluster].sort_values('new_score').head(size_cluster).index.tolist()
        else:
            if index_ in data[data['cluster']==cluster].sort_values('new_score').head(5).index.tolist():
                lis_index = data[data['cluster']==cluster].sort_values('new_score').head(6).index.tolist()
                lis_index = lis_index.remove(index)
            else:
                lis_index = data[data['cluster']==cluster].sort_values('new_score').head(5).index.tolist()

        recommendations = info.iloc[lis_index]
    return movie, recommendations
def print_(string):
    # Format de print
    separator = "---------------------------"
    print(separator + " " + string + " " + separator)
    return
def normalize(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    np_scaled = min_max_scaler.fit_transform(data)
    data_normalized = pd.DataFrame(np_scaled)
    return data_normalized
#%%
def init():
    data = pd.read_csv('movie_metadata.csv', sep=",")
    global info_2
    global data_2
    data_2, info_2 = cleanAndSelect_v2(data)
    data_2_norm = normalize(data_2)
    pca = decomposition.PCA(n_components = 12)
    pca.fit(data_2_norm)
    data_2_trans = pca.transform(data_2_norm)
    pca.explained_variance_ratio_.sum()
    kmeans = KMeans(n_clusters=200).fit(data_2_trans)
    labels = pd.Series(kmeans.labels_,index = data_2.index.tolist())
    info_2 = pd.concat([info_2, labels.to_frame('cluster')], axis = 1)
    data_2 = pd.concat([data_2, labels.to_frame('cluster')], axis = 1)
    return
def getRecommendation(film_id):
    movie, recommendations = recommend_clustering(data_2, info_2, film_id)
    if movie is None or recommendations is None:
        res = 'Sorry, we are not able to recommend you a movie based on the selected movie'
    else:
        selected_columns_display = ['movie_title', 'genres','director_name','title_year']
        res = movie[selected_columns_display].to_string(index=False,header=False) +
        res += ' ------------------ '
        res += recommendations[selected_columns_display].to_string(index=False,header=False)
    return res
