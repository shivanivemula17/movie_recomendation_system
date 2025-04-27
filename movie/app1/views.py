import numpy as np
import pickle
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse

# Load the pre-trained movie recommendation model


movies_dict = pickle.load(open('app1/movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

def get_movie_names(request):
    movie_titles = (movies['title'].values).tolist()
    return JsonResponse(movie_titles, safe=False)

similarity = pickle.load(open('app1/similarity.pkl','rb'))

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

def predict(request):
    if request.method == "POST":
        movie_name = request.POST.get("movie_name")
        recommendations=recommend(movie_name)
        return render(request, "index.html", {"movies": recommendations})
    return render(request, "index.html", {})


 