import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
KEY = getenv("API_KEY")

def get_movies(title):
    url = "https://www.omdbapi.com/"
    params = {
        "apikey": KEY,
        "s": title
    }

    response = requests.get(url, params=params)
    data = response.json()

    result = []

    for i in data["Search"]:
        movie = {}
        movie["Title"] = f'{i["Title"]} ({i["Year"]})'
        movie["Type"] = i["Type"].capitalize()
        movie["IMDb"] = i["imdbID"]
        result.append(movie)
    
    return result

def get_data(id):
    url = "https://www.omdbapi.com/"
    params = {
        "apikey": KEY,
        "i": id
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data