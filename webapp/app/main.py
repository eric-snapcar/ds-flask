# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:29:25 2017

@author: ATruong1
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from scipy import sparse # Need this to create a sparse array
from sklearn.preprocessing import StandardScaler
import ast
import datetime
#%%
def charge():
    #chargement des données
    data_ = pd.read_csv('data/data_tronque_global.csv', sep=",",error_bad_lines=False)
    coefs_ = pd.read_csv('data/coefs_global.csv', sep=",",error_bad_lines=False)
    data_ref = pd.read_csv('data/ref_airport.csv', sep=",",error_bad_lines=False)
    dic_airport = pd.read_csv('data/dic_airport.csv', sep=",",error_bad_lines=False)
    data_carrier = pd.read_csv('data/data_carrier.csv', sep=",",error_bad_lines=False)

    coefs = coefs_['INTERCEPT_COEFS'][1:]
    intercept = coefs_['INTERCEPT_COEFS'][0]
    dic_airport = ast.literal_eval(dic_airport['ORIGIN_NUM'][0])
    list_flight = data_['FLIGHT'].drop_duplicates().tolist()

    #préparation des variables
    scalingDF = data_[['DISTANCE', 'CRS_ELAPSED_TIME']].astype('float') # Numerical features
    categDF = data_[['MONTH', 'DAY_OF_WEEK', 'ORIGIN_NUM',
                    'DEST_NUM', 'ARR_HOUR', 'DEP_HOUR',
                    'CARRIER_CODE']]
    return data_, data_ref, coefs, intercept, list_flight, scalingDF, categDF, dic_airport, data_carrier

def display(originCity,originCode,destCity,destCode,date,depHour,prediction):
    return 'The flight from {} ({}) to {} ({}) on {} at {} will have a delay of {} min'.format(originCity,originCode,destCity,destCode,date,depHour,prediction)

def predict(origin, destination, carrier_code, date, hour_departure, data_, data_ref, list_flight, dic_airport, scalingDF, categDF, coefs, intercept):
    flight = origin +'|'+destination+'|'+carrier_code
    day = int(date.split('/')[0])
    month = int(date.split('/')[1])
    day = datetime.datetime(2017, month, day)
    day_of_week = day.weekday()+1

    if flight in list_flight:
        elapsed_time = data_[data_['FLIGHT'] == flight]['CRS_ELAPSED_TIME'].mean()
        distance = data_[data_['FLIGHT'] == flight]['DISTANCE'].mean()
        arrival_time = hour_departure + round(elapsed_time/60)
        origin_num = dic_airport[origin]
        dest_num = dic_airport[destination]
        carrier = data_carrier[data_carrier['UNIQUE_CARRIER'] == carrier_code]['CARRIER_CODE'].values[0]
        scale = pd.DataFrame([(distance, elapsed_time)], columns =['DISTANCE', 'CRS_ELAPSED_TIME'])
        categ = pd.DataFrame([(month, day_of_week, origin_num, dest_num, arrival_time, hour_departure, carrier)], columns = ['MONTH', 'DAY_OF_WEEK', 'ORIGIN_NUM', 'DEST_NUM', 'ARR_HOUR', 'DEP_HOUR', 'CARRIER_CODE'])
    else:
        print('The flight does not exist, please check again your flight info:')
        print('     Origin and Destination Airport Code are written in a 3 letter capital format')
        print('     Carrier is 2 letter/number capital format')
        print('     Carrier is 2 letter/number capital format')
        print('     Date is in the format DD/MM')

    encoder = OneHotEncoder() # Create encoder objec
    encoder.fit(categDF)
    categDF_encoded = encoder.transform(categ)
    scaler = StandardScaler() # create scaler object
    scaler.fit(scalingDF)
    scalingDF_sparse = sparse.csr_matrix(scaler.transform(scale)) # Transform the data and convert to sparse
    x_to_predict = sparse.hstack((scalingDF_sparse, categDF_encoded))
    y_predicted = x_to_predict.toarray().dot(coefs) + intercept
    y_predicted = round(y_predicted[0])
    return display(data_ref[data_ref['CODE']==origin].iloc[0]['CITY'],origin,data_ref[data_ref['CODE']==destination].iloc[0]['CITY'],destination,date,hour_departure,y_predicted)
#%%
def init():
    global data_, data_ref, coefs, intercept, list_flight, scalingDF, categDF, dic_airport, data_carrier
    data_, data_ref, coefs, intercept, list_flight, scalingDF, categDF, dic_airport, data_carrier = charge()
    return


#%%
def test():
    return predict('ATL', 'BOS', 'DL', '12/12', 16, data_, data_ref, list_flight, dic_airport, scalingDF, categDF, coefs, intercept)


#%%
#data_, data_ref, coefs, intercept, list_flight, scalingDF, categDF, dic_airport, data_carrier = charge()
#print test()
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
