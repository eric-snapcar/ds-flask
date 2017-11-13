# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:29:11 2017
@author: ATruong1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 09:20:04 2017
@author: ATruong1
"""
#%%
import pandas as pd
from sklearn import preprocessing
from pandas import get_dummies
from sklearn import decomposition
from scipy.spatial.distance import pdist, squareform
#%%
def cleanAndSelect_vf(data):
    #selectionne les variables listées dans car_selected ['var1', 'var2', 'var3'],
    var_selected =['language','num_voted_users','actor_1_name','actor_2_name','actor_3_name','imdb_score','genres','duration','director_name']

    data_ = data[['movie_title','title_year']+var_selected]
    data_ = data_.dropna()
    data_ = data_.drop_duplicates(['movie_title','title_year'])
    data_.index.name = 'film_id'
    data_ = data_.reset_index()
    info = data_
    data_ = data_[var_selected].copy()


    #Ajout des réalisateurs et des langues
    data_ = addColumnForEachContent(data_,'director_name', 0)
    data_ = addColumnForEachContent(data_,'language', 0)

    #Ajout des genres
    data_ = addColumnForEachWord(data_,'genres', 0)

    #Ajout des Acteurs (présence de l'acteur dans le film 1 ou 0, peu importe Acteur1, Acteur 2, Acteur3)
    data_['actors']= data_['actor_1_name']+'|'+data_['actor_2_name']+'|'+data_['actor_3_name']
    data_ = addColumnForEachWord(data_,'actors', 0)
    data_ = data_.drop(['actor_1_name','actor_3_name','actor_2_name'], axis=1)

    #Nouveau score qui sublime les haut score avec beaucoup de votes et pénalise les score faibles avec beaucoup de vote
    score_ = (data['imdb_score']-data['imdb_score'].mean()).divide(10)
    num_voter_ = data['num_voted_users'].divide(data['num_voted_users'].max())
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
def distance_matrix(data):
    #Calcule une matrice de distance euclidienne entre toutes les lignes de 'data'
    dist_ = pdist(data, 'euclidean')
    dist_ = pd.DataFrame(squareform(dist_))
    return dist_
def getRecommendation_(index_bis , info, distanceMatrix):
    # renvoie les 5 éléments les plus proches de 'index_bis' dans 'distance_matrix'
    nsmallest_list = distanceMatrix.nsmallest(6, index_bis).index.values.tolist()
    del nsmallest_list[0]
    res = info.iloc[nsmallest_list]
    return res
def recommend(data, info, film_id, d_matrix):
    #Renvoie les films recommandés par la fonction 'getRecommend'
    index = info.index[info['film_id'] == film_id].tolist()
    if len(index) == 0:
        return None, None
    else:
        index_ = index[0]
    movie = info.iloc[[index_]]
    recommendations = getRecommendation_(index_,info,d_matrix)
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
def pca_trans(data_norm, n_components):
    pca = decomposition.PCA(n_components)
    pca.fit(data_norm)
    data_trans = pca.transform(data_norm)
    pca.explained_variance_ratio_.sum()
    return data_trans
def print_var(data, info = None):
    #Affiche les variables dans le dataframe df, le data type, ainsi que les 5 premiers éléments si 'afficher'='oui'

    print('Variables')
    print()
    for var in list(data):
        print('-------------------------------------------------')
        #print(var,' (',df[var].dtype,')','     ',df[var][0],',',df[var][1],',',df[var][2],',',df[var][3],',',df[var][4]) # A améliorer
        print(var,' (',data[var].dtype,')','      ')
        if info == 'oui':
            print(data[var][0:4])
    print('-------------------------------------------------')
    print()
    print('Le nombre de variables est de :',len(list(data)))
    return
#%%
init_ = False
def init():
    global init_
    init_ = True
    data = pd.read_csv('data.csv', sep=",")
    global info_f
    global dmatrix_f
    global data_f
    data_f, info_f = cleanAndSelect_vf(data)
    data_f_norm = normalize(data_f)
    dmatrix_f = distance_matrix(data_f_norm)
    data = None
    return

def getRecommendation(film_id):
    if init_:
        movie, recommendations = recommend(data_f, info_f, film_id, dmatrix_f)
        return movie, recommendations
    else:
        return None, None
