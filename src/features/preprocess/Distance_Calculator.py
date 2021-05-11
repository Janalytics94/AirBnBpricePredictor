#!/usr/bin/env python3
import pandas as pd 

import geopy
from geopy.distance import geodesic


class Distance_Calculator:
    ''' class to calculate distance between airbnb of a chosen point in London
    df : dataframe of interest
    long_poi : takes the longitue of the point of interest
    lat_poi : takes the lattitude of the point of interest
    
    ''' 

    def zip_objects(self, df, long_poi, lat_poi):
        ''' Zip those objects'''
        df = df[['longitude', 'latitude']]
        df['longPoi'] = long_poi
        df['latPoi'] = lat_poi
        df['originCoordinates'] = list(zip(df['latitude'], df['longitude']))
        df['poiCoordinates'] = list(zip(df['latPoi'],df['longPoi']))

        return df    

    def get_distance(self,originCoordinates, poiCoordinates):
        ''' calculate distance between the origin and point of interest'''
        dist = geopy.distance.geodesic(originCoordinates, poiCoordinates).km

        return dist
    







