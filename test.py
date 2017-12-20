# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:29:25 2017

@author: ATruong1
"""
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from scipy import sparse # Need this to create a sparse array
from sklearn import linear_model
#%%
def charge():
    #chargement des données
    data_ = pd.read_csv('data_flight_delay_2016.csv', sep=",",error_bad_lines=False)
    list_para = pd.read_csv('list_para.csv', sep=",",error_bad_lines=False)
    data_ref = pd.read_csv('ref_airport.csv', sep=",",error_bad_lines=False)

    #préparation des variables
    data_['FLIGHT'] = data_['ORIGIN'].astype('str') + '|' + data_['DEST'].astype('str') + '|' + data_['UNIQUE_CARRIER'].astype('str')
    scalingDF = data_[['DISTANCE', 'CRS_ELAPSED_TIME']].astype('float') # Numerical features
    categDF = data_[['MONTH', 'DAY_OF_MONTH', 'FLIGHT', 'ARR_HOUR', 'DEP_HOUR']]
    list_flight = data_['FLIGHT'].value_counts()
    list_flight_filtered = list_flight[(list_flight>364)].index.values.tolist()
    return data_, data_ref, list_para, list_flight_filtered, scalingDF, categDF
def predict(origin, destination, carrier_code, date, hour_departure, hour_arrival, data_, data_ref, list_para, list_flight_filtered, scalingDF, categDF):
    flight = origin +'|'+destination+'|'+carrier_code
    day = int(date.split('/')[0])
    month = int(date.split('/')[1])
    flightDF =[]
    flightDF.insert(0, {'MONTH': month, 'DAY_OF_MONTH': day, 'FLIGHT': flight, 'ARR_HOUR': hour_arrival, 'DEP_HOUR': hour_departure})
    if flight in list_flight_filtered:
        categDF_flight = pd.concat([pd.DataFrame(flightDF),categDF[data_['FLIGHT'] == flight]], ignore_index = True).drop('FLIGHT', axis = 1)
    else:
        print('The flight does not exist, please check again your flight info:')
        print('     Origin and Destination Airport Code are written in a 3 letter capital format')
        print('     Carrier is 2 letter/number capital format')
        print('     Carrier is 2 letter/number capital format')
        print('     Date is in the format DD/MM')

    encoder = OneHotEncoder() # Create encoder objec
    categDF_encoded = encoder.fit_transform(categDF_flight)
    x_topredict = sparse.csr_matrix(categDF_encoded.toarray()[0])
    x_train = sparse.csr_matrix(categDF_encoded.toarray()[1:])
    y_train = data_[data_['FLIGHT'] == flight]['ARR_DELAY'].values

    l1_ratio_ = list_para[list_para['flight']==flight]['l1_ratio'].iloc[0]
    alpha_ = list_para[list_para['flight']==flight]['alpha'].iloc[0]
    SGD_model = linear_model.SGDRegressor(penalty='elasticnet', alpha = alpha_ ,l1_ratio = l1_ratio_)
    SGD_model.fit(x_train, y_train)

    y_predicted = SGD_model.predict(x_topredict)
    print('The flight from ',data_ref[data_ref['CODE']==origin]['CITY'],' (',origin,') to ',data_ref[data_ref['CODE']==destination]['CITY'], ' (',destination,') on ',date,' at ',hour_departure,'will have a delay of ',y_predicted[0],' min')
    return
#%%
def init():
    global data_, data_ref, list_para, list_flight_filtered, scalingDF, categDF
    data_, data_ref, list_para, list_flight_filtered, scalingDF, categDF = charge()
    return
def getPrediction(origin, destination, carrier_code, date, hour_departure, hour_arrival):
    predict(origin, destination, carrier_code, date, hour_departure, hour_arrival, data_, data_ref, list_para, list_flight_filtered, scalingDF, categDF)
    return
init()
print(data_.head())
print(getPrediction("DFW", "DTW", "AA", "20/01", 11, 14))
"""
   Unnamed: 0  MONTH  DAY_OF_MONTH  DAY_OF_WEEK UNIQUE_CARRIER ORIGIN DEST  \
0           0      1             6            3             AA    DFW  DTW
1           1      1             7            4             AA    DFW  DTW
2           2      1             8            5             AA    DFW  DTW
3           3      1             9            6             AA    DFW  DTW
4           4      1            10            7             AA    DFW  DTW

   ARR_DELAY  CRS_ELAPSED_TIME  DISTANCE  DEP_HOUR  ARR_HOUR      FLIGHT
0       -6.0             158.0     986.0        11        14  DFW|DTW|AA
1      -12.0             158.0     986.0        11        14  DFW|DTW|AA
2        7.0             158.0     986.0        11        14  DFW|DTW|AA
3       -5.0             158.0     986.0        11        14  DFW|DTW|AA
4      113.0             158.0     986.0        11        14  DFW|DTW|AA
"""
