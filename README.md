# AirBnB Price Predictor
## Kaggle Competition Adams SS2021

To get full access to the whole project please download the zip ADAMS_AIRBNB_604930 from the following Link: https://drive.google.com/file/d/14TU1WHxr1R7huOkWBidrZQLKwzhPm7HZ/view?usp=sharing

# Usage Docker
```
 docker build . -t airbnb 
 docker run -it --name airbnb -v $(pwd):/root/ airbnb bash

```

## Usage model with .dvc

```
 dvc init --no-scm
 dvc repro -f

```

## Usage model with python 
You can call the model by using a listing_id from the test data set.

```
 ./src/models/predict.py 0FEMC4VA5U
```