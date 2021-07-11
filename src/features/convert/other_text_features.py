#!/usr/bin/env python3

import os 
import sys
import pandas as pd 
import numpy as np
sys.path.append('.')
from src.features.convert.amenities_dict import amenities_dict
import src.features.preprocess.Textprocessor as Textprocessor
import src.features.preprocess.Processor as Processor
import csv
import json
import requests
import langdetect

from langdetect import detect
from time import sleep
from clize import run

def clean_amenities(source, target):
    
    df_names = ['train', 'test']
    for df_name in df_names:
        if df_name == 'train':
            df = pd.read_csv(os.path.join(source + '/'+ df_name + '.csv'), index_col='listing_id')
            df = df[df.amenities != '{}']
            df['amenities'] = df['amenities'].apply(lambda x: x.replace('{', '').replace('}', '').replace('"','').split(','))
            df['amenities'] = df['amenities'].apply(lambda x:','.join(x))
            amenities = np.unique(np.concatenate(df['amenities'].map(lambda amns: amns.split(",")).values))
            amenities_matrix = np.array([df['amenities'].map(lambda amns: amn in amns).values for amn in amenities])
            amenities_df = pd.DataFrame(data=amenities_matrix.T, columns=amenities, index=df.index)
            amenities_df = amenities_df.drop(columns=['translation missing: en.hosting_amenity_49', 'translation missing: en.hosting_amenity_50' ])
            amenities_df = amenities_df.rename(columns=amenities_dict)
            amenities_df = amenities_df.loc[:,~amenities_df.columns.duplicated(keep='last')]
            amenities_df.to_csv(os.path.join(target + '/' + df_name + '/' + 'amenities_'+ df_name + '.csv'))

        else:
            df = pd.read_csv(os.path.join(source + '/'+ df_name + '.csv'), index_col='listing_id')
            df['amenities'] = df['amenities'].apply(lambda x: x.replace('{', '').replace('}', '').replace('"','').split(','))
            df['amenities'] = df['amenities'].apply(lambda x:','.join(x))
            amenities = np.unique(np.concatenate(df['amenities'].map(lambda amns: amns.split(",")).values))
            amenities_matrix = np.array([df['amenities'].map(lambda amns: amn in amns).values for amn in amenities])
            amenities_df = pd.DataFrame(data=amenities_matrix.T, columns=amenities, index=df.index)
            amenities_df = amenities_df.drop(columns=['', 'translation missing: en.hosting_amenity_49', 'translation missing: en.hosting_amenity_50' ])
            amenities_df = amenities_df.rename(columns=amenities_dict)
            amenities_df = amenities_df.loc[:,~amenities_df.columns.duplicated(keep='last')]
            amenities_df.to_csv(os.path.join(target + '/' + df_name + '/' + 'amenities_'+ df_name + '.csv'))

    return 

def process_other_text_features(source, target):
    text_processor = Textprocessor()
    processor = Processor()
    df_names = ['train', 'test']
    for df_name in df_names:
        with open(os.path.join(source + '/'  + df_name + '.csv'), newline='') as csvfile:
            with open(os.path.join(target + '/' + df_name + '/' + df_name + '.jsonl'), 'w') as out_file:
                data =csv.DictReader(csvfile)
                lines = list(data) # adapt it to 0 so it will run through 
                for i in range(0, len(lines)):
                    row = lines[i]
                #for row in data:
                    listing_id = row['listing_id']
                    name = row['name']
                    description = row['description']
                    transit = row['transit']
                    house_rules = row['house_rules']
                    neighborhood_overview = row['neighborhood_overview']
                    length = len(description)
                    try:
                        # detect_language
                        language = detect(description)
                        if language != 'en':
                            try:
                            # translate 
                                name = text_processor.translate(name)
                                description = text_processor.translate(description)
                                transit = text_processor.translate(transit)
                                house_rules = text_processor.translate(house_rules)
                                neighborhood_overview = text_processor.translate(neighborhood_overview)

                            except (requests.exceptions.ConnectionError) as e:
                                print('Too Many Requests, let me sleep for 10 seconds...')
                                sleep(10)
                                continue

                    except langdetect.lang_detect_exception.LangDetectException:
                        print('No features in text...')
                        continue
                    except json.JSONDecodeError:
                        pass
                    
                    # clean
                    name = text_processor.clean(name)
                    name = text_processor.remove_URL(name)
                    name = text_processor.convert_emojis_to_word(name)
                    # clean
                    description  = text_processor.clean(description )
                    description  = text_processor.remove_URL(description )
                    description  = text_processor.convert_emojis_to_word(description )
                # clean
                    transit = text_processor.clean(transit)
                    transit = text_processor.remove_URL(transit)
                    transit = text_processor.convert_emojis_to_word(transit)
                # clean
                    house_rules = text_processor.clean(house_rules)
                    house_rules = text_processor.remove_URL(house_rules)
                    house_rules = text_processor.convert_emojis_to_word(house_rules)

                    neighborhood_overview = text_processor.clean(neighborhood_overview)
                    neighborhood_overview = text_processor.clean(neighborhood_overview)
                    neighborhood_overview = text_processor.clean(neighborhood_overview)
                
                    # process 
                    lemmas_name, common_words_name = text_processor.process(name)
                    # process 
                    lemmas_description, common_words_description = text_processor.process(description)
                    lemmas_transit, common_words_transit = text_processor.process(transit)
                    lemmas_house_rules, common_words_house_rules =  text_processor.process(house_rules)
                    lemmas_neighborhood_overview, common_words_neighborhood_overview =  text_processor.process(neighborhood_overview)

                    # get_sentiments
                    # all texts as texts could play a crucial role only strings with more then 10 characters
                    if length >= 10:
                        json.dump(
                            {
                                'listing_id': listing_id,
                                'name':  name,
                                'description': description,
                                'transit': transit,
                                'house_rules': house_rules,
                                'neighborhood_overview': neighborhood_overview,
                                'language': language,
                                'lemmas_name': lemmas_name,
                                'common_words_name': common_words_name,
                                'lemmas_description': lemmas_description,
                                'common_words_description': common_words_description,
                                'lemmas_transit': lemmas_transit,
                                'common_words_transit': common_words_transit,
                                'lemmas_house_rules': lemmas_house_rules,
                                'common_words_house_rules': common_words_house_rules,
                                'lemmas_neighborhood_overview': lemmas_neighborhood_overview,
                                'common_words_neighborhood_overview': common_words_neighborhood_overview
                                }, out_file
                        )
                        out_file.write('\n')
                    
    return
                

if __name__=='__main__':
    run(clean_amenities)#process_other_text_features

