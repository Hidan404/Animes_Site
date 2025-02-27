from Api import get_all_animes
from sessao import carregar_sessao, salvar_sessao
from streamlit_carousel import carousel
import streamlit as st
from banco_de_dados import iniciar_bd, login_usuario, registrar_usuario



st.set_page_config(page_title="Animes Atuais", layout="wide")


if "logged_in" not in st.session_state:
    sessao_salva = carregar_sessao()
    st.session_state["logged_in"] = sessao_salva.get("logged_in", False)
    st.session_state["username"] = sessao_salva.get("username", None)

if st.button("🔴 Sair"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    salvar_sessao({"logged_in": False, "username": ""})  # Limpa a sessão
    st.rerun()  # Recarrega a págin

st.markdown("### 🌗 Alternância de Tema")
st.write("Para mudar entre **Modo Claro e Escuro**, clique no menu de configurações (☰) no canto superior direito e escolha o tema desejado.")

iniciar_bd()
menu = ["Login", "Registrar", "Animes", "Minha Lista","Imagens Animes"]
choice = st.sidebar.selectbox("Menu", menu)

if "favoritos" not in st.session_state:  # ADICIONADO
    st.session_state["favoritos"] = []

if choice == "Login":
    st.subheader("🔑 Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if login_usuario(username, password):
            st.success(f"Bem-vindo {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username

            salvar_sessao({"logged_in": True, "username": username})
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
        
        search_query = st.text_input("🔍 Pesquisar Anime", "")
        
        animes = get_all_animes()

        # Criar lista de gêneros únicos
        generos_disponiveis = []
        for anime in animes:
            for genre in anime.get('genres', []):
                if genre['name'] not in generos_disponiveis:
                    generos_disponiveis.append(genre['name'])

        genero_escolhido = st.selectbox("🎭 Filtrar por Gênero", ["Todos"] + generos_disponiveis)            

        # Aplicar filtros antes da paginação
        if search_query:
            animes = [anime for anime in animes if search_query.lower() in anime.get('title', '').lower()]

        if genero_escolhido != "Todos":
            animes = [anime for anime in animes if any(g['name'] == genero_escolhido for g in anime.get('genres', []))]

        # Se nenhum anime foi encontrado, exibe aviso e interrompe execução
        if not animes:
            st.warning("Nenhum anime encontrado com os filtros aplicados.")
            st.stop()

        st.markdown("<h1 style='text-align: center; font-family: Cursive; margin-bottom: 1rem'>📺 Animes da Temporada</h1>", unsafe_allow_html=True)
        
        # Configurar paginação
        if "page" not in st.session_state:
            st.session_state.page = 1 

        animes_por_pagina = 10  
        total_paginas = max(1, (len(animes) // animes_por_pagina) + 1)

        inicio = (st.session_state.page - 1) * animes_por_pagina
        fim = inicio + animes_por_pagina
        animes_paginados = animes[inicio:fim]


       

        # Exibir animes filtrados e paginados
        for anime in animes_paginados:
            col1, col2 = st.columns([1, 3])
            with col1:
                image_url = anime.get('images', {}).get('jpg', {}).get('image_url', 'default_image.jpg')
                st.image(image_url, width=150)
            with col2:
                st.subheader(anime.get('title', 'Título não disponível'))
                synopsis = anime.get('synopsis', 'Sinopse não disponível') or "Sinopse não disponível"
                st.write(synopsis[:200] + "...")
                aired_date = anime.get('aired', {}).get('from', 'Data não disponível')
                st.write(f"📅 Estreia: {aired_date[:10]}")
                st.write(f"⭐ Nota: {anime.get('score', 'Sem nota')}")

                trailer_url = anime.get('trailer', {}).get('url')
                if trailer_url:
                    st.video(trailer_url)  # Exibe o vídeo diretamente
                else:
                    st.write("🎥 Sem trailer disponível.")

                st.link_button("Mais detalhes", anime.get('url', '#'))


                if st.button(f"Favoritar 🌟 {anime.get('title')}"):
                    if anime not in st.session_state["favoritos"]:
                        st.session_state["favoritos"].append(anime)
                        st.success(f"{anime.get('title')} adicionado aos favoritos!")
                    else:
                        st.warning(f"{anime.get('title')} já está na sua lista de favoritos!")

        # Botões de paginação
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
        st.warning("Faça login para ver os animes!")

elif choice == "Minha Lista":  
    st.subheader("🌟 Minha Lista de Favoritos")
    if "favoritos" in st.session_state and st.session_state["favoritos"]:
        for anime in st.session_state["favoritos"]:
            st.write(f"- {anime.get('title')}")
    else:
        st.warning("Nenhum anime foi favoritado ainda.")        

elif choice == "Imagens Animes":

    st.markdown(
    """
    <style>
        .carousel img {
            width: 400px !important;
            height: 250px !important;
            object-fit: cover !important;
            border-radius: 10px;
        }
        .main {
            max-width: 1200px;
            margin: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    animes = get_all_animes()  # Chamando a função corretamente
    imagens = []

    for anime in animes:
        image_url = anime.get("images", {}).get("jpg", {}).get("large_image_url", "https://via.placeholder.com/300")
        titulo = anime.get('title', 'Título Desconhecido')  # Garantindo um título
        descricao = anime.get('synopsis', 'Descrição não disponível')  # Garantindo descrição

        imagens.append({
            "title": titulo,
            "text": descricao,
            "img": image_url
        })

    # Certifique-se de que a lista está corretamente formatada
    

    carousel(imagens) 
