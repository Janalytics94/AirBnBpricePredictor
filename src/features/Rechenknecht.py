#!/usr/bin/env python3

# This Skript is for very computationally intensive steps and safes the desided output to a file because we don't want to run it every time
import pandas as pd
import numpy as np
from src.Distance_Calculator import Distance_Calculator
from src import helpers
import src.features.preprocess.ImageProcessor as ImageProcessor

train = helpers.read_df('data/train.csv', index_col='listing_id')
train = helpers.change_data_types(train)

longlat = Distance_Calculator().zip_objects(train,lat_poi=51.510067,long_poi=-0.133869)
longlat['dist'] = [dist_calc.get_distance(**longlat[['originCoordinates','poiCoordinates']].iloc[i].to_dict()) for i in range(longlat.shape[0])]
longlat.to_csv('data/processed/longlat.csv')

images = ImageProcessor.ImageProcessor.getImages('data/images/*.png')
imgData  = [ImageProcessor.ImageProcessor.imgDetails(image) for image in images]
brightness = [ImageProcessor.ImageProcessor.getBrightness(image) for image in images]
colors_BGR = [ImageProcessor.ImageProcessor.channelSplit(image) for image in images]