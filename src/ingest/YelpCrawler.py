#! /usr/bin/env python3 

import pandas as pd
import json
import requests
from time import sleep

from clize import run

def crawl_yelp(target):
    '''Crawls RestAPI of Yelp to get additional data for Neighbour Hoods'''
    api_key = 'dJ2fEA6y23SK0QhGgIweg0eOimGYx9IPTOeKg58GtUOMhSFN9qXJ82Q0WvNDSD_iiAg1CRUubPGa797eREBDQQpejqgQQVXj3R1qOSU2ARMEWduAWOfGOultbdqTYHYx'
    # We check the Endpoint business/ Get Method API
    url = 'https://api.yelp.com/v3/businesses/search'
   
     # what do we want 
    price = []
    rating = []
    coordinates = [] # might be useful later
    zip_codes = []

    headers = {'Authorization': 'Bearer %s' % api_key}

    offset = 0
     
    ## loop to iterate over 200 pages of 500 businesses each = 100000 businesses in London 
    while offset <=1:
        try:
            params={'term':'Restaurants', 'location': 'london', 'limit': 50, 'offset': offset}
            req = requests.get(url, params=params, headers=headers)
            parsed = json.loads(req.text)
        except requests.exceptions.ConnectionError as e:
            print('Too Many Requests, let me sleep for 10 seconds...')
            sleep(10)
            continue
        # KANN MAN NOCH SCHICKER MACHEN
        n = 0
        while n <= 50:
            try:
                price_data = parsed["businesses"][n]['price']
                ratings_data = parsed["businesses"][n]['rating']
                zipcode_data = parsed["businesses"][n]["location"]["zip_code"]
                coordinates_data = parsed['businesses'][n]['coordinates']
                
                rating.append(ratings_data)
                zipcode.append(zipcode_data)
                prices.append(price_data)
                coordinates.append(coordinates_data)
                
            except:
                ## some of the data gathered are not going to have the necessary information
                ## so we skip those 
                pass
        offset += 1
    
    #Create dataframe of crawled data
    yelp_df = pd.DataFrame({'rating': rating, 'zipcodes': zipcode, 'prices': prices, 'coordinates': coordinates}) 
    yelp_df.to_csv(target)

    return

if __name__ == '__main__':
    run(crawl_yelp)
