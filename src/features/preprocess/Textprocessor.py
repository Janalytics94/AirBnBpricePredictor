#!/usr/bin/env python3

import spacy

class TextProcessor():
    ''' Class to initilaize text processing '''
    def __init__(self):

    def get_data(self,df):
        '''remove missing values / nan in texts'''
        columns = df.columns.tolist()
        if 'description ' in columns:
            clean = df[pd.isna(train.description)==False]
            text = clean.description.values.tolist()
        else 'comment' in columns:
            clean = df[pd.isna(reviews.comment)==False]
            text = clean.comment.values.tolist()

        return text

    def description_length(self,df):
        ''' Calculates Description Length of each Airbnb'''
        df['description_length'] = df.description.apply(lambda x: len(x))

        return df


    def process(self,text):
        ''' NLP on text data '''
        
        nlp = spacy.load("en_core_web_sm")
        docs = [nlp(text) for text in text]
        tokens = [token for token in doc for doc in docs]
        # remove stopwords
        filtered = [token for token in tokens if not token.is_stop]
        lemmas = [f"Token: {token}, lemma: {token.lemma_}" for token in filtered]
        
        return filtered, lemmas
    # def get_ngrams


    # def textbloop    
