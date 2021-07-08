#!/usr/bin/env python3

import json 
import os 
import pandas as pd 
import sys
import numpy as np
sys.path.append('.')

import src.features.preprocess.Textprocessor as Textprocessor
import src.features.preprocess.Processor as Processor
import src.features.preprocess.DistanceCalculator as DistanceCalculator

from sklearn.cluster import KMeans
from clize import run


def rechenknecht(source, target):
    ''' creates all important features and cleans source dataframes
    params:
    - source: takes in the source data path 
    - target: takes in the target data path after cleansing safe the dataframe in data/interim
    '''
    df_names = ['train', 'test']
    # Initialize all important classes
    processor = Processor()
    textprocessor = Textprocessor()
    distanceCalculator = DistanceCalculator()
    
    
    for df_name in df_names:
        # Use processing types for standard preprocessing
        df = pd.read_csv(os.path.join(source+'/'+ df_name + '.csv'), index_col='listing_id')
        columns = df.columns.tolist()
        df = processor.change_data_types(df)
        df = processor.NaNs(df)
        df = processor.membership(df)
        df = processor.host_response_rate_to_probabilities(df)
        df = processor.effect_coding_host_response_time(df)
        df = textprocessor.text_length(df)
        df = processor.impute_review_scores(df)
        if 'price' in columns:
            df['log_price'] = df.price.apply(lambda x: processor.price_log_transformation(x))
            price = np.array(df.price)
            price = price.reshape(-1,1)
            kmeans = KMeans(n_clusters=3).fit(price.reshape(-1,1))
            price_labels = kmeans.predict(price.reshape(-1,1))
            centers = kmeans.cluster_centers_
            df['price_cluster'] = price_labels
        
       

        # Distances 
        longlat = distanceCalculator.zip_objects(df,lat_poi=51.510067,long_poi=-0.133869)
        longlat['dist'] = [distanceCalculator.get_distance(**longlat[['originCoordinates','poiCoordinates']].iloc[i].to_dict()) for i in range(longlat.shape[0])]
        df = pd.concat([longlat['dist'], df], axis = 1)
        df = df.drop(['latitude','longitude'], axis = 1)
        df = processor.drop_features(df)
        df = processor.get_relevant_features(df)
        df = processor.clean_cancellation_policy(df)
        df = processor.hot_encode(df)
        
        
    
        df.to_csv(os.path.join(target + '/' + df_name + '/' + df_name + '.csv'))

if __name__=='__main__':
    run(rechenknecht)



    
