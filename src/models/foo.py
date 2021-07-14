#!/usr/bin/env python3
# Usual imports
import numpy as np
import pandas as pd
import string
import matplotlib.pyplot as plt
import concurrent.futures
import time
import pyLDAvis.sklearn
import plotly.plotly as py
import warnings
import plotly.graph_objs as go
import plotly.figure_factory as ff
import ast


# spaCy based imports
import spacy
warnings.filterwarnings('ignore')

%matplotlib inline
import os

from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
from tqdm import tqdm
from pylab import bone, pcolor, colorbar, plot, show, rcParams, savefig
from plotly import tools

# Plotly based imports for visualization
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from gensim.models import Word2Vec
from collections import Counter
  
nlp = spacy.load("en_core_web_sm")


df = pd.read_csv('/root/data/interim/train/texts.csv', index_col='listing_id')
df['lemmas_name'] = df['lemmas_name'].apply(lambda x: x.strip(" ]' ' '[" " ").split(','))
df['lemmas_description'] = df['lemmas_description'].apply(lambda x: x.strip("]' ' '[" " ").split(','))
df['lemmas_transit'] = df['lemmas_transit'].apply(lambda x: x.strip("]' ' '[" " ").split(','))
df['lemmas_house_rules'] = df['lemmas_house_rules'].apply(lambda x: x.strip("]' ' '[" " ").split(','))
df['lemmas_neighborhood_overview'] = df['lemmas_neighborhood_overview'].apply(lambda x: x.strip("]' ' '[" " ").split(','))

filter_col = [col for col in df if col.startswith('lemmas')]
df = df[filter_col]
df['lemmas_name'] = [[df.lemmas_name[j][i].strip(" ' ") for i in range(0,len(df.lemmas_name[j]))] for j in range(0,len(df.lemmas_name))]
df['lemmas_description'] = [[df.lemmas_description[j][i].strip(" ' ") for i in range(0,len(df.lemmas_description[j]))] for j in range(0,len(df.lemmas_description))]
df['lemmas_transit'] = [[df.lemmas_transit[j][i].strip(" ' ") for i in range(0,len(df.lemmas_transit[j]))] for j in range(0,len(df.lemmas_transit))]
df['lemmas_house_rules'] = [[df.lemmas_house_rules[j][i].strip(" ' ") for i in range(0,len(df.lemmas_house_rules[j]))] for j in range(0,len(df.lemmas_house_rules))]
df['lemmas_neighborhood_overview'] = [[df.lemmas_neighborhood_overview[j][i].strip(" ' ") for i in range(0,len(df.lemmas_neighborhood_overview[j]))] for j in range(0,len(df.lemmas_neighborhood_overview))]

data = df.lemmas_name.values

# Calculating DF 
DF = {}
for i in range(len(data)):
    tokens = data[i]
    for w in tokens:
        try:
            DF[w].add(i)
        except:
            DF[w] = {i}

for i in DF:
    DF[i] = len(DF[i])

DF

total_vocab=[x for x in DF]
len(total_vocab)

def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c


doc = 0
N=len(df)
tf_idf = pd.DataFrame()

for i in range(N):
    
    tokens = data[i]
    
    counter = Counter(tokens + data[i])
    words_count = len(tokens + data[i])
    
    for token in np.unique(tokens):
        
        tf = counter[token]/words_count
        df = doc_freq(token)
        idf = np.log((N+1)/(df+1))
        
        tf_idf[doc, token] = tf*idf

    doc += 1

alpha = 0.3
for i in tf_idf:
    tf_idf[i] *= alpha

test = tf_idf.toarray()

tf_idf[(0, 'greenwich')]
list(tf_idf.keys())[4]
len(tf_idf)
tf_idf.keys()
df = pd.DataFrame(tf_idf, index=df.index)
df.columns = df.columns.str.strip('()').str.split(',', expand=True)
print (df)



print (df.columns)
MultiIndex(levels=[['1515', '42', '4312'], ['32', '5135', '56']],
           labels=[[0, 1, 2], [0, 2, 1]])