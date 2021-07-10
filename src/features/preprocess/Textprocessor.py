#!/usr/bin/env python3
# URLS
import pandas as pd
import requests
import numpy as np
from time import sleep

# NLP in general
import spacy
from collections import Counter
from spacytextblob.spacytextblob import SpacyTextBlob

# to handle different langauges in reviews
from google_trans_new import google_translator
# emojies
import pickle
import re


class Textprocessor():
    ''' Class to initilaize text processing '''

    def get_data(self,df, column):
        '''remove missing values / nan in texts'''
        if column == 'description':
            clean = df[pd.isna(df.column)==False]
            #text = clean.description.values.tolist()
        if column == 'comments':
            clean = df[pd.isna(df.column)==False]
           #text = clean.comment.values.tolist()

        return clean

    def text_length(self, df):
        ''' Calculates Description Length, House_rule Length and Transit Length of each Airbnb & drops those who only have '''

        df['description_length'] = df.description.apply(lambda x: len(x))
        df['transit_length'] = df.transit.apply(lambda x: len(x))
        df['house_rules_length'] = df.house_rules.apply(lambda x: len(x))
        df['neighborhood_length'] = df.neighborhood_overview.apply(lambda x: len(x))

        return df
    
    def outlier_trunctuation(self, df, factor):
        
        IQR = df[column].quantile(0.75) - df[column].quantile(0.25) 
        # factor = 1.5
        upper = df[column].quantile(0.75) + factor*IQR
        lower = df[column].quantile(0.25) - factor*IQR
        df_new = df.copy()
        df_new = df_new.loc[(df.all_text_length < lower) | (df.all_text_length > upper)]
            
        return df_new, IQR

    def translate(self, text):
        ''' Translates reviews in different languages to english'''

        translator = google_translator()
        trans_text = translator.translate(text)
        

        return trans_text      

    def convert_emojis_to_word(self, text):
        ''' uses Emoji_Dict.p as bases to convert existing emojis to words to prevent loss of information'''

        with open('/root/data/external/Emoji_Dict.p', 'rb') as fp:
            Emoji_Dict = pickle.load(fp)
        Emoji_Dict = {v: k for k, v in Emoji_Dict.items()}
        for emot in Emoji_Dict:
            text = re.sub(r'('+emot+')', "_".join(Emoji_Dict[emot].replace(",","").replace(":","").split()), text)
        
        return text    


    def clean(self, text):
        ''' 
        Removes unnessary stuff from text like numbers, punctuation, etc. from data set turn everything to lower case
        '''

        text = text.replace("\r","")
        text = text.replace("\n","")
        text = text.replace("\\","")
        text = text.replace("/", "")
        text = text.replace("/", "")
        text = re.sub('[?@#$\&+!*"-]', '', text)
        text = re.sub('£', '', text)
        text = re.sub(r'[0-9]', '', text)
        text = re.sub('\s+',' ', text)
        text = text.strip('/')
        text = text.strip('{')
        text = text.strip('}')
        text = text.strip('(')
        text = text.strip(')')
        text = text.lower()

        return text   

    def remove_URL(self, text):
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

        return text


    def process(self, text):
        ''' Basic NLP on text data (remove stopwords, lemmatizations, tokens) might need some additional work'''
        
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text) 
        tokens = [token for token in doc]
        # remove stopwords
        filtered = [token for token in tokens if not token.is_stop]
        # remove puntuations
        filtered = [token for token in filtered if not token.is_punct]
        # remove white spaces 
        filtered = [token for token in filtered if not token.is_space ]
        # lemmatize and turn it to lowercase
        lemmas = [token.lemma_.strip().lower() for token in filtered]
        word_freq = Counter(lemmas)
        # 5 commonly occurring words with their frequencies
        common_words = word_freq.most_common(5)

        return lemmas, common_words
    
    def get_sentiments(self,review):
        ''' Sentimentsanalyse'''

        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("spacytextblob")
        #Stopwords
        stpw = spacy.lang.en.stop_words.STOP_WORDS
        doc = nlp(review)
        tokens = [token for token in doc]
        # remove stopwords
        filtered = [token for token in tokens if not token.is_stop]
        # remove puntuations
        filtered = [token for token in filtered if not token.is_punct]
        # remove white spaces 
        filtered = [token for token in filtered if not token.is_space ]

        assessments = doc._.assessments 
        subjectivity = doc._.subjectivity
        polarity = doc._.polarity 

        return assessments, subjectivity, polarity
    
    def aggregate_review_data(self,df):
        ''' 
        aggregates the features gathered from reveiw_data
        '''
        df['mean_polarity'] = df.groupby(df.index)['polarity'].mean()
        df['review_count'] = df.groupby(df.index)['review_id'].count()

       # fill up missing values 
       #f df = df.fillna(0)

        return df
        

       
