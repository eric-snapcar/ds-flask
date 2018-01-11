# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:29:25 2017

@author: ATruong1
"""
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from scipy import sparse # Need this to create a sparse array
from sklearn.preprocessing import StandardScaler
import ast
import datetime
from dateutil.parser import parse
from sklearn.externals import joblib
#%%
def charge():
    #chargement des données
    list_flight = pd.read_csv('list_flight.csv', sep=",",error_bad_lines=False)
    coefs_ = pd.read_csv('coefs_global_.csv', sep=",",error_bad_lines=False)
    data_ref = pd.read_csv('ref_airport.csv', sep=",",error_bad_lines=False)
    dic_airport = pd.read_csv('dic_airport.csv', sep=",",error_bad_lines=False)
    data_carrier = pd.read_csv('data_carrier.csv', sep=",",error_bad_lines=False)
    encoder = joblib.load('encoding.pkl')
    scaler = joblib.load('scaling.pkl')

    coefs = coefs_['INTERCEPT_COEFS'][1:]
    intercept = coefs_['INTERCEPT_COEFS'][0]
    dic_airport = ast.literal_eval(dic_airport['ORIGIN_NUM'][0])


    #préparation des variables
    #scalingDF = data_[['DISTANCE', 'CRS_ELAPSED_TIME', 'HDAYS']].astype('float') # Numerical features
#==============================================================================
#     categDF = data_[['MONTH', 'DAY_OF_WEEK', 'ORIGIN_NUM',
#                     'DEST_NUM', 'ARR_HOUR', 'DEP_HOUR',
#                     'CARRIER_CODE', 'WEEK']]
#==============================================================================
    return data_ref, coefs, intercept, list_flight, dic_airport, data_carrier, encoder, scaler

def display(originCity,originCode,destCity,destCode,date,depHour,prediction):
    return 'The flight from {} ({}) to {} ({}) on {} at {} will have a delay of {} min'.format(originCity,originCode,destCity,destCode,date,depHour,prediction)

def predict_(origin, destination, carrier_code, date, hour_departure, data_ref, list_flight, dic_airport, coefs, intercept, encoder, scaler):
    flight = origin +'|'+destination+'|'+carrier_code
    day = int(date.split('/')[0])
    month = int(date.split('/')[1])
    date = datetime.datetime(2017, month, day)
    day_of_week = date.weekday()+1

    holidays_2017 = ['2017-01-02', '2017-01-16','2017-02-20','2017-05-29',
                     '2017-07-04','2017-09-04','2017-10-09','2017-11-10','2017-11-23',
                     '2017-12-25', '2018-01-01']
    list_holidays_2017 = [parse(x) for x in holidays_2017]
    if flight in list_flight['FLIGHT'].tolist():
        elapsed_time = list_flight[list_flight['FLIGHT'] == flight]['CRS_ELAPSED_TIME'].mean()
        distance = list_flight[list_flight['FLIGHT'] == flight]['DISTANCE'].mean()
        arrival_time = hour_departure + round(elapsed_time/60)
        origin_num = dic_airport[origin]
        dest_num = dic_airport[destination]
        carrier = data_carrier[data_carrier['UNIQUE_CARRIER'] == carrier_code]['CARRIER_CODE'].values[0]
        holi = 1/(min([abs((datetime.datetime(2017, month, day)-y).days) for y in list_holidays_2017])+1)
        week = datetime.datetime(2017, month, day).isocalendar()[1]
        scale = pd.DataFrame([(distance, elapsed_time,holi)], columns =['DISTANCE', 'CRS_ELAPSED_TIME','HADAYS'])
        categ = pd.DataFrame([(month, day_of_week, origin_num, dest_num, arrival_time, hour_departure, carrier, week)], columns = ['MONTH', 'DAY_OF_WEEK', 'ORIGIN_NUM', 'DEST_NUM', 'ARR_HOUR', 'DEP_HOUR', 'CARRIER_CODE', 'WEEK'])
    else:
        error = 'The flight does not exist, please check again your flight info:\n'+'Origin and Destination Airport Code are written in a 3 letter capital format\n'+'Carrier is 2 letter/number capital format\n'+'Carrier is 2 letter/number capital format\n'+'Date is in the format DD/MM'
        json_ = {'error':error}
        return json.dumps(json_)
    #encoder = OneHotEncoder() # Create encoder objec
    #encoder.fit(categDF)
    categDF_encoded = encoder.transform(categ)
    #scaler = StandardScaler() # create scaler object
    #scaler.fit(scalingDF)
    scalingDF_sparse = sparse.csr_matrix(scaler.transform(scale)) # Transform the data and convert to sparse
    x_to_predict = sparse.hstack((scalingDF_sparse, categDF_encoded))
    y_predicted = x_to_predict.toarray().dot(coefs) + intercept
    y_predicted = round(y_predicted[0])
    """
    if y_predicted < 0:
        print('The flight from ',data_ref[data_ref['CODE']==origin]['CITY'],' (',origin,') to ',data_ref[data_ref['CODE']==destination]['CITY'], ' (',destination,') on ',date.strftime('%Y-%m-%d'),' at ',hour_departure,'o\'clock will have an advance of ',-1*y_predicted,' min')
    else:
        print('The flight from ',data_ref[data_ref['CODE']==origin]['CITY'],' (',origin,') to ',data_ref[data_ref['CODE']==destination]['CITY'], ' (',destination,') on ',date.strftime('%Y-%m-%d'),' at ',hour_departure,'o\'clock will have a delay of ',y_predicted,' min')
    """
    originCity = data_ref[data_ref['CODE']==origin]['CITY'].name
    originCode = origin
    destCity = data_ref[data_ref['CODE']==destination]['CITY'].name
    destCode = destination
    date = date.strftime('%Y-%m-%d')
    hour = hour_departure
    prediction = y_predicted
    json_ = {'origin' : origin , 'originCity':originCity,'destination':destination, 'carrier':carrier_code,'destinationCity' : destCity, 'date' :date,'hour':hour,'value':prediction}
    return json.dumps(json_)
#%%


def init():
    global data_ref, coefs, intercept, list_flight, dic_airport, data_carrier, encoder, scaler
    data_ref, coefs, intercept, list_flight, dic_airport, data_carrier, encoder, scaler = charge()
    return
def predict(origin, destination, carrier_code, day,month, hour_departure):
    return predict_(origin, destination, carrier_code, day+"/"+month, int(hour_departure), data_ref, list_flight, dic_airport, coefs, intercept, encoder, scaler)
#%%
#data_ref, coefs, intercept, list_flight, dic_airport, data_carrier, encoder, scaler = charge()
#%%
def test():
    return predict('ATL', 'BOS', 'DL', '12/12', 16)


#%%
#init()
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
