#! /usr/bin/env python3 
import pandas as pd 
import urllib.request
import os 
import sys 
import time

from clize import run
from urllib.error import HTTPError

def crawl_images(source,df_name, target):
    ''' Crawls all the images provided from the url and safes them into a folder
    params:
    - source: takes in the data path 
    - df_name: either test.csv or train.csv
    - target : path to image data storage
    '''
    # load in data set
    path = os.path.join(source + df_name) 
    df = pd.read_csv(path, index_col='listing_id')
    # get picture url
    pictures = df.picture_url
    # start crawling
    start = time.time()
    for i in range(0,len(pictures)):
        try:
            urllib.request.urlretrieve(pictures.iloc[i], target + pictures.index[i] + '.png')
        except HTTPError as e:
            print('Picture does not exist')
            continue
    ende = time.time()
    print('{:5.3f}s'.format(ende-start)) 
    df.drop('picture_url', axis=1)
    df.to_csv('data/interim/' + df_name)    
    
    return

if __name__ == '__main__':
    run(crawl_images)