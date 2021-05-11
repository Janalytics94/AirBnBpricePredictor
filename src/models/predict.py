#!/usr/bin/env python3

import os 
import pandas as pd

from clize import run 

from sklearn.linear_model import LinearRegression

#def predict(source, target):

train = pd.read_csv('data/canonical/train/train.csv', index_col='listing_id')
test = pd.read_csv('data/canonical/test/test.csv', index_col='listing_id')
len(test)
test.isnull().sum()
test = test.dropna()


train = train[train.isnull()!=True]
train = train.dropna()
len(train)
target = train.price
train = train.drop('price', axis=True)
len(train)
len(target)
reg = LinearRegression().fit(train, target)
reg.score(train, target)
predictions = reg.predict(test)
predictions = pd.Series(predictions, index=test.index, name='price')
predictions
index = pd.Series(test.index)
index
predictions = pd.concat([index, predictions], axis=1) 
# W
predictions
predictions.to_csv('predictions/sample_submission.csv')