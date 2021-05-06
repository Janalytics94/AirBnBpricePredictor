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

# Considerung information on restaurants as well using yelp
# https://towardsdatascience.com/ai-and-real-state-renting-in-amsterdam-part-1-5fce18238dbc




# BUT AIRBNB is more for holiday so Piccadally circus should be fine
# If you are analysing a bigger city that has multiple locations that are considered desirable, you can also run this code as many times as needed with different geographical points. (Don’t forget to change the column names so you don’t overwrite the previous point!).
For example, there is a financial district close to the Amsterdam Zuid station that could be equally (or even more) relevant to working tenants than living close to the city center. Measuring these various scenarios is more important if you are using methods similar to multiple linear regressions rather than machine-learning statistical algorithms because they are inherently better at recognising non-linear relationships and clusters. For this reason, I won’t include it in this analysis but it is an interesting factor to weight in depending on the statistical method being used.
