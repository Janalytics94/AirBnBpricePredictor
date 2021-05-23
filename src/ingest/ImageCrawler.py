#! /usr/bin/env python3 
import pandas as pd 
import urllib.request
import os 
import sys 
#TODO: Another library beautifulsoup!

import time

from clize import run
from urllib.error import HTTPError
from urllib.error import ContentTooShortError

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
            urllib.request.urlretrieve(pictures.iloc[i], target + df_name + pictures.index[i] + '.png')
        except HTTPError or ContentTooShortError as e:
            print('Picture does not exist or we are not able to crawl it')
            continue
    ende = time.time()
    print('{:5.3f}s'.format(ende-start))  
    
    return
    #urllib.error.ContentTooShortError: <urlopen error retrieval incomplete: got only 25616 out of 40886 bytes>

if __name__ == '__main__':
    run(crawl_images)