from Api import get_all_animes
import streamlit as st
from banco_de_dados import iniciar_bd, login_usuario, registrar_usuario

st.set_page_config(page_title="Animes Atuais", layout="wide")

iniciar_bd()
menu = ["Login", "Registrar", "Animes"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("🔑 Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if login_usuario(username, password):
            st.success(f"Bem-vindo {username}!")
            st.session_state["logged_in"] = True
        else:
            st.error("Credenciais inválidas")

elif choice == "Registrar":
    st.subheader("📝 Criar Conta")
    new_user = st.text_input("Usuário")
    new_pass = st.text_input("Senha", type="password")
    if st.button("Registrar"):
        registrar_usuario(new_user, new_pass)
        st.success("Usuário criado! Faça login.")

elif choice == "Animes":
    if "logged_in" in st.session_state:
        
        animes = get_all_animes()

        if animes:  
            st.markdown("<h1 style='text-align: center; font-family: Cursive; margin-bottom: 1rem'>📺 Animes da Temporada</h1>", unsafe_allow_html=True)

            
            if "page" not in st.session_state:
                st.session_state.page = 1 

            animes_por_pagina = 10  
            total_paginas = (len(animes) // animes_por_pagina) + 1

            
            inicio = (st.session_state.page - 1) * animes_por_pagina
            fim = inicio + animes_por_pagina
            animes_paginados = animes[inicio:fim]

            
            for anime in animes_paginados:
                col1, col2 = st.columns([1, 3])
                with col1:
                    image_url = anime.get('images', {}).get('jpg', {}).get('image_url', 'default_image.jpg')
                    st.image(image_url, width=150)
                with col2:
                    st.subheader(anime.get('title', 'Título não disponível'))
                    synopsis = anime.get('synopsis', 'Sinopse não disponível')

                    if synopsis == None:
                        synopsis = 'Sinopse não disponível'
                    else:
                        synopsis =  synopsis[:200] + "..."  

                    st.write(synopsis)
                    aired_date = anime.get('aired', {}).get('from', 'Data não disponível')
                    st.write(f"📅 Estreia: {aired_date[:10]}")
                    st.write(f"⭐ Nota: {anime.get('score', 'Sem nota')}")
                    st.link_button("Mais detalhes", anime.get('url', '#'))

        
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                if st.session_state.page > 1:
                    if st.button("⬅ Página Anterior"):
                        st.session_state.page -= 1
                        st.rerun()

            with col3:
                if st.session_state.page < total_paginas:
                    if st.button("Próxima Página ➡"):
                        st.session_state.page += 1
                        st.rerun()
        else:
            st.error("Não foi possível carregar a lista de animes.")
    else:
        st.warning("Faça login para ver os animes!")
