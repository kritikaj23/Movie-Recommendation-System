# -*- coding: utf-8 -*-
"""Movie Recommendation System

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bbk1fVAcKmVia7pJPcg1_fsd6hJsYxbt
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px

dataC= pd.read_csv('/content/credits.csv')
datam= pd.read_csv('/content/movies.csv')

dataC.head()

datam.head()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

dataC

datam

datam.head()

dataC.head()

datam=datam.merge(dataC, on='title')

datam.shape

datam.head()

datam.info()



datam=datam[['movie_id','title','overview','genres','keywords','cast','crew']]

datam.head()

datam.info()

datam.isnull().sum()

datam.dropna(inplace=True)

datam.duplicated().sum()

datam.iloc[0].genres

import ast

def convert(obj):
  L=[]
  for i in ast.literal_eval(obj):
    L.append(i['name'])
  return L

datam['keywords']=datam['keywords'].apply(convert)
datam.head()

def convert3(obj):
  L=[]
  counter=0
  for i in ast.literal_eval(obj):
    if counter!=3:
      L.append(i['name'])
      counter+=1
    else:
      break
  return L

datam['cast']=datam['cast'].apply(convert3)

datam.head()

def fetch_director(obj):
  L=[]
  for i in ast.literal_eval(obj):
    if i['job']=='Director':
      L.append(i['name'])
      break
  return L

datam['crew']=datam['crew'].apply(fetch_director)

datam.head()

datam['overview'][0]

datam['overview'][3]

datam['overview']=datam['overview'].apply(lambda x:x.split())

datam['overview'][1]

datam['genres']=datam['genres'].apply(lambda x:[i.replace(" ","") for i in x])

datam['keywords']=datam['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
datam['cast']=datam['cast'].apply(lambda x:[i.replace(" ","") for i in x])
datam['crew']=datam['crew'].apply(lambda x:[i.replace(" ","") for i in x])

datam

datam['tags']=datam['overview']+datam['genres']+datam['keywords']+datam['cast']+datam['crew']

datam

newm=datam[['movie_id','title','tags']]

newm

newm['tags']=newm['tags'].apply(lambda x:" ".join(x))

newm

newm['tags'][0]

newm['tags']=newm['tags'].apply(lambda x:x.lower())

newm.head()

newm['tags'][0]

from sklearn.feature_extraction.text import CountVectorizer #keyword text into a vector on the basis of frequency count ech word occurs in the entire text
cv=CountVectorizer(max_features=5000,stop_words='english')

cv.fit_transform(newm['tags']).toarray().shape

vectors=cv.fit_transform(newm['tags']).toarray()

vectors[0]

len(cv.get_feature_names_out())

import nltk

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

newm['tags']=newm['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity

cosine_similarity(vectors)

cosine_similarity(vectors).shape

similarity=cosine_similarity(vectors)

similarity[0]

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

def recommend(movie):
  movie_index=newm[newm['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movies_list:
    print(newm.iloc[i[0]].title)

pip install ipywidgets

import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import numpy as np

# Assuming `newm` DataFrame with real movie titles
newm = pd.read_csv('movies.csv')  # Load your DataFrame with real movie titles

# Example similarity matrix (replace with your actual similarity matrix)
similarity = np.random.rand(len(newm), len(newm))
similarity = (similarity + similarity.T) / 2  # make it symmetric
np.fill_diagonal(similarity, 1)

def recommend(movie):
    movie_index = newm[newm['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_movies = [newm.iloc[i].title for i, _ in sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]]
    return recommended_movies

# Create autocomplete text box
autocomplete = widgets.Combobox(
    placeholder='Select or type a movie title...',
    options=newm['title'].tolist(),
    description='Movie:',
    ensure_option=True,
    continuous_update=False
)

# Create output widget
output = widgets.Output()

# Define event handler
def on_movie_change(change):
    with output:
        output.clear_output()
        recommendations = recommend(change.new)
        print("Recommendations:")
        for rec in recommendations:
            print(rec)

# Attach event handler
autocomplete.observe(on_movie_change, names='value')

# Display widgets
display(autocomplete, output)

recommend('Spider-Man 3')
