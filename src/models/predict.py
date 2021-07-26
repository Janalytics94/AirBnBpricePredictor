#!/usr/bin/env python3
from xgboost import XGBRegressor

class AirbnbPricePredictor():
    ''' Holds the final method to predict prices of Airbnb's in London'''

    def __init__(self):
        model = XGBRegressor()
        model.load_model('../data/models/xgb.json')
        
    def predict(self, listing_id): #'0FEMC4VA5U'
        predictions = model.predict(X_test, ntree_limit=model.best_ntree_limit)
        predictions = pd.Series(predictions.ravel(), index=test.index, name='price')
        predictions = predictions.apply(lambda x: np.exp(x))
        price = predictions.filter(like=listing_id)[0]
        
        return print('The predicted price of this Airbnb is: ' + str(round(price,2)) + " £.")


if __name__ == "__main__":
    airbnb = AirbnbPricePredictor()
    airbnb.predict('0FEMC4VA5U')
