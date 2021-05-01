#! /usr/bin/env python3 
import pandas as pd 
import urllib.request
import os 
import sys 
import time
from clize import run

def crawl_images(source, target):
    ''' Crawls all the images provided from the url and safes them into a folder'''
    # load in data set
    path = os.path.join(source + 'train.csv') 
    train = pd.read_csv(path, index_col='listing_id')
    # get picture url
    _pUrl_list = train.picture_url.unique().tolist()
    filenames = train.index.unique().tolist()
    # start crawling
    start = time.time()
    for url in _pUrl_list:
        for filename in filenames:
            urllib.request.urlretrieve(url, target + filename + '.png')
    ende = time.time()
    print('{:5.3f}s'.format(ende-start))     
    
    return

if __name__ == '__main__':
    run(crawl_images)