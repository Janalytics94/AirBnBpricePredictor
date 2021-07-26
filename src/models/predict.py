#! /usr/bin/env python3
import os
import xgboost
from xgboost import XGBRegressor
from clize import run

def predict(listing_id):
    ''' Holds the final method to predict prices of Airbnb's in London'''
    listing_id = str(listing_id)
    model = XGBRegressor()
    model.load_model(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "data/models/xgb.json"))
    test = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "data/canonical/test/test.csv"), index_col='listing_id')
    predictions = model.predict(test, ntree_limit=model.best_ntree_limit)
    predictions = pd.Series(predictions.ravel(), index=test.index, name='price')
    predictions = predictions.apply(lambda x: np.exp(x))
    price = predictions.filter(like=listing_id)[0]
    
    return print('The predicted price of this Airbnb is: ' + str(round(price,2)) + " £.")


if __name__ == "__main__":
    run(predict)
