# AirBnB Price Predictor
## Kaggle Competition Adams SS2021
```
docker build . -t airbnb 
docker run -it --name airbnb -v $(pwd):/root/ airbnb bash

```

## Usage model with .dvc

```
 dvc repro -f

```

## Usage model with python 
You can call the model by using a listing_id from the test data set.

```
 ./src/models/predict.py 0FEMC4VA5U
```