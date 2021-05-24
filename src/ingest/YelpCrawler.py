#! /usr/bin/env python3 

import pandas as pd
import json
import requests
from time import sleep

api_key = 'dJ2fEA6y23SK0QhGgIweg0eOimGYx9IPTOeKg58GtUOMhSFN9qXJ82Q0WvNDSD_iiAg1CRUubPGa797eREBDQQpejqgQQVXj3R1qOSU2ARMEWduAWOfGOultbdqTYHYx'
# We check the Endpoint business/ Get Method API
url = 'https://api.yelp.com/v3/businesses/search'

    # what do we want 
price = []
rating = []
coordinates = [] # might be useful later
zipcodes = []

headers = {'Authorization': 'Bearer %s' % api_key}
    
## loop to iterate over 20000 pages of 50 businesses each = 100000 businesses in London 
for offset in range(0,20000):
    try:
        params={'term':'Restaurants', 'location': 'london', 'limit': 50, 'offset': offset}
        req = requests.get(url, params=params, headers=headers)
        parsed = json.loads(req.text)
    except requests.exceptions.ConnectionError as e:
        print('Too Many Requests, let me sleep for 10 seconds...')
        sleep(10)
        continue
    for n in range(0,50):
        try:
            # Hätte man wahrscheinlich schneller über css Selektorwn hinbekommen
            price_data = parsed["businesses"][n]['price']
            ratings_data = parsed["businesses"][n]['rating']
            zipcode_data = parsed["businesses"][n]["location"]["zip_code"]
            coordinates_data = parsed['businesses'][n]['coordinates']
            
            rating.append(ratings_data)
            zipcodes.append(zipcode_data)
            price.append(price_data)
            coordinates.append(coordinates_data)
        except KeyError as e:
            pass
            
#Create dataframe of crawled data
a = {'rating': rating, 'zipcodes': zipcodes, 'prices': price, 'coordinates': coordinates}
df = pd.DataFrame.from_dict(a, orient='index')
df = df.transpose()
df.to_csv('/root/data/external/yelp.csv')

