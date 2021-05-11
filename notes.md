# TODO
## Check Crawlers
## Consider Test Data as well nd think about that when you consider calculating steps!
### überarbeite docker image but not so important at first 

## EDA , check correlation between features, check for multicollinearity etc, vernünftige plots auswählen
    - Ngrams, text blobs Decription etc
## Feature Engineering
    - distance to center (Piccadally Circus) --> get foto of that point in map! other districts might be useful if you work there but Airbnb is usually for holiday #done
    - Host since in years  #done
    - Host is super host might be important, also information about the host if its very detailed Airbnbs might be popular
    - analyze yelp data --> also EDA ? 
    - Text Länge 
    - Sentiment Analyse reveiws --> multiple languages
    - Image Preprocessing 
## Feature Selection
    - Check Feature Importance 
    - Grid Search 
## Models
    - Benchmark different Models for regression (probably)
    --- Multi Linear Regression 
    --- Neural Networks 
    - Model Evaluation
    - Choose final method
## Hyperparameter Tuning

## Safe Data and Conclusion/ Outlook 
  -- Yelp data was useful or not , outlook price dropping Time Series Analysis 

# References


# Notes along with Data Analysis
Description of Airbnb almost the same as summary but longer and more informative
14 airbnbs have no name airbnb[pd.isna(airbnb.name)==True]
1726 airbnbs no Description --> wahrscheinlich am besten für main part der Text analyse
2954 airbnbs no summary --> column weglassen (?)

For text data definetly description and space

1062 airbnb[airbnb.experiences_offered!='none'] drop it for analysis ?

Features : 

host since __ berechnen 
IMporttant Feature Calculating distance to the city center using longitude and lattitude!
(description l)

reviews -> senitmentäts analyse for multi languages
location -> je zentraler desto besser
summary -> len(zeichenkette), je detailierter die Beschreibung, höherer Preis etc.


# alle host haben ein Profile picture yay

# Reviews
Sentiments analyse but how to handle the different languages?

https://towardsdatascience.com/ai-and-real-state-renting-in-amsterdam-part-1-5fce18238dbc
papers im ornder uni/AirbnbPrediction
https://philmohun.medium.com/making-models-airbnb-price-prediction-feature-engineering-and-unstructured-image-analysis-8f0456663fd8
https://www.analyticsvidhya.com/blog/2019/08/3-techniques-extract-features-from-image-data-machine-learning-python/
https://medium.com/reputation-com-datascience-blog/keywords-extraction-with-ngram-and-modified-skip-gram-based-on-spacy-14e5625fce23
# Considerung information on restaurants as well using yelp
# https://towardsdatascience.com/ai-and-real-state-renting-in-amsterdam-part-1-5fce18238dbc




# BUT AIRBNB is more for holiday so Piccadally circus should be fine
# If you are analysing a bigger city that has multiple locations that are considered desirable, you can also run this code as many times as needed with different geographical points. (Don’t forget to change the column names so you don’t overwrite the previous point!).
For example, there is a financial district close to the Amsterdam Zuid station that could be equally (or even more) relevant to working tenants than living close to the city center. Measuring these various scenarios is more important if you are using methods similar to multiple linear regressions rather than machine-learning statistical algorithms because they are inherently better at recognising non-linear relationships and clusters. For this reason, I won’t include it in this analysis but it is an interesting factor to weight in depending on the statistical method being used.

## use open CV for immage detection 
#Taking a step back, we can think of a few things in images that may impact the price:
#- Are the floors carpet or hardwood?
#- Are the walls painted or wallpaper? Paintings or posters?
#- Does the host have plants? Are they alive and healthy?
#- Is the picture well-lit and inviting?

#To keep our scope narrow, we will pull four values from the image that may be of value:
#Brightness je mehr licht desto besser
#2. # of red pixels
#3. # of blue pixels
#4. # of green pixels

