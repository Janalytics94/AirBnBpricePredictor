#!/usr/bin/env python3

# NLP in general
import spacy
# to handle different langauges in reviews
from google_trans_new import google_translator
# emojies
import pickle
import re

class TextProcessor():
    ''' Class to initilaize text processing '''

    def get_data(self,df):
        '''remove missing values / nan in texts'''

        columns = df.columns.tolist()
        if 'description ' in columns:
            clean = df[pd.isna(train.description)==False]
            text = clean.description.values.tolist()
        if 'comment' in columns:
            clean = df[pd.isna(reviews.comment)==False]
            text = clean.comment.values.tolist()

        return text

    def description_length(self, df):
        ''' Calculates Description Length of each Airbnb'''

        df['description_length'] = df.description.apply(lambda x: len(x))

        return df

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
        ''' Removes \n and \r from data set turn everything to lower case'''

        text = text.replace("\r\n\\\t","")
        text = text.lower()

        return text     

    def process(self, text):
        ''' Basic NLP on text data (remove stopwords, lemmatizations, tokens) might need some additional work'''
        
        nlp = spacy.load("en_core_web_sm")
        docs = [nlp(text) for text in text]
        tokens = [token for token in doc for doc in docs]
        # remove stopwords
        filtered = [token for token in tokens if not token.is_stop]
        lemmas = [f"Token: {token}, lemma: {token.lemma_}" for token in filtered]
        
        return filtered, lemmas
       
