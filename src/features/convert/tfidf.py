#!/usr/bin/env python3
# Usual imports
import numpy as np
import pandas as pd
import os


# spaCy based imports
import spacy

# scipy
import scipy.sparse
from collections import Counter

# sklearn
import sklearn
from sklearn.feature_extraction import DictVectorizer
from clize import run

def tf_idf(source, target):

    '''
    Function that calculates TF_IDF for each text feature in train and test data
    '''
    nlp = spacy.load("en_core_web_sm")
    #source = 'data/interim'
    #target = 'data/tmp'

    def doc_freq(word):
        c = 0
        try:
            c = DF[word]
        except:
            pass
        return c
        
    df_names = ['train', 'test']
    for df_name in df_names: 
        df = pd.read_csv(os.path.join(source, df_name, 'texts.csv'), index_col='listing_id')
        listing_ids = df.index.values
        filter_col = [col for col in df if col.startswith('lemmas')]
        df = df[filter_col]
        for col in filter_col: 
            df[col] = df[col].apply(lambda x: x.strip(" ]' ' '[" " ").split(','))
            df[col] = [[df[col][j][i].strip(" ' ") for i in range(0,len(df[col][j]))] for j in range(0,len(df[col]))]
            array = df[col].values
           
        # Calculate DF & TF_IDF
            DF = {}
            for i in range(len(array)):
                tokens = array[i]
                for w in tokens:
                    try:
                        DF[w].add(i)
                    except:
                        DF[w] = {i}
            
            for i in DF:
                DF[i] = len(DF[i])
                total_vocab = [x for x in DF]
            print('Total Vocab Size is '+ str(len(total_vocab)))
            
            
            # CALC TF_IDF
            doc = 0
            N = len(df)
            tf_idf = {}

            for i in range(N):
                tokens = array[i]
                counter = Counter(tokens + array[i])
                words_count = len(tokens + array[i])
                for listing_id in listing_ids:
                    for token in np.unique(tokens):
                        tf = counter[token]/words_count
                        df = doc_freq(token)
                        idf = np.log((N+1)/(df+1))
                        tf_idf[doc, listing_id, token] = tf*idf

                    doc += 1
                    alpha = 0.3
                    for i in tf_idf:
                        tf_idf[i] *= alpha
                    v = DictVectorizer(dtype=float, sparse=True)
                    sparse_matrix = v.fit_transform(tf_idf)
                    scipy.sparse.save_npz(os.path.join(target, df_name , 'sparse_matrix_{0}.npz').format(col), sparse_matrix)
    return


if __name__=='__main__':
    run(tf_idf)


