import requests
import streamlit as st


@st.cache_data
def get_all_animes():
    animes = []
    limit = 50  # Quantidade de animes por requisição
    page = 1
    
    while True:
        # Fazendo a requisição à API da Jikan com paginação
        response = requests.get(f"https://api.jikan.moe/v4/seasons/now?page={page}")
        
        if response.status_code == 200:
            data = response.json()
            current_animes = data.get('data', [])
            
            if not current_animes:  # Se não houver mais animes, interrompa o loop
                break
            
            animes.extend(current_animes)  # Adiciona os animes da página atual à lista de animes
            page += 1  # Avança para a próxima página
        else:
            print(f"Erro na requisição: {response.status_code}")
            break  # Interrompe se ocorrer erro

    return animes
