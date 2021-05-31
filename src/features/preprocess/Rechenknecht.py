#! /usr/bin/env python3
# This Skript is for very computationally 
#intensive steps and safes the desided output to a 
# interim files because we don't want to run it every time
import spacy
import pandas as pd
import numpy as np
import os

from ImageProcessor import ImageProcessor
from Textprocessor import TextProcessor
from Distance_Calculator import Distance_Calculator
from Processor import Processor

from clize import run


def rechenknecht(source, images, target):
    ''' creates all important features and cleans source dataframes
    params:
    - source: takes in the data path 
    - df_name: either test.csv or train.csv
    - source_images: dirctory where all the crawled images are stored
    - target_longlat : path to safe interim results
    - target_images : path to safe interim results
    - target_processed_df: after cleansing safe the dataframe in data/interim
    '''
    df_names = ['train', 'test']
    # Initialize all important classes
    processor = Processor()
    distanceCalculator = Distance_Calculator()
    imageProcessor = ImageProcessor()
    textprocessor  = TextProcessor()
    
    for df_name in df_names:
        # Use processing types for standard preprocessing
        df = pd.read_csv(os.path.join(source+'/'+ df_name + '.csv'), index_col='listing_id')
        df = processor.change_data_types(df)
        df = processor.NaNs(df)


        # Distances 
        longlat = distanceCalculator.zip_objects(df,lat_poi=51.510067,long_poi=-0.133869)
        longlat['dist'] = [distanceCalculator.get_distance(**longlat[['originCoordinates','poiCoordinates']].iloc[i].to_dict()) for i in range(longlat.shape[0])]
        df = pd.concat([longlat['dist'], df], axis = 1)
        df = df.drop(['latitude','longitude'], axis = 1)
    
        # Images 
        images = imageProcessor.getImages(os.path.join(source + '/' + df_name))
        imgData  = [imageProcessor.imgDetails(image) for image in images]
        brightness = [imageProcessor.getBrightness(image) for image in images]
        colors_BGR = [imageProcessor.channelSplit(image) for image in images]

        ImageData = pd.DataFrame({'ImageData': imgData, 'Brightness': brightness, 'BGR': colors_BGR})
        df = pd.concat([ImageData,df], axis =1)
        df = df.drop(['picture_url'], axis = 1)
    

        # Membership
        df = processor.membership(df)
        df = df.drop(['host_since_year','host_since'], axis = 1)

        
        # Text Data
        # Preprocess description 
        #Get Clean Data Description
        df = textprocessor.description_length(df)
        # drop space and summary as they seem to be a mix of description
        df = df.drop(['space', 'summary'], axis = 1)
        
        df.to_csv(os.path.join(target + '/'+ df_name + '.csv'))
    
    return

if __name__ == '__main__':
    run(rechenknecht)

