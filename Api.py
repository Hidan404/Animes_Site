import requests

api_url = "https://api.jikan.moe/v4/seasons/now"

def get_animes(api = api_url):
    resposta = requests.get(api)
    if resposta.status_code == 200:
        return resposta.json().get("data", [])
    return []

get_animes()