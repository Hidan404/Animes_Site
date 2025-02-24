from Api import get_all_animes
import streamlit as st
from banco_de_dados import iniciar_bd, login_usuario, registrar_usuario



st.set_page_config(page_title= "Animes Atuais", layout= "wide")

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

        if animes:  # Verifique se a lista de animes não está vazia
            st.markdown("<h1 style='text-align: center; font-family: Cursive; margin-bottom: 1rem'>📺 Animes da Temporada</h1>", unsafe_allow_html=True)

            for anime in animes:
                if anime:  # Verifique se o objeto 'anime' não é None
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        # Verificando se a imagem está presente
                        image_url = anime.get('images', {}).get('jpg', {}).get('image_url', 'default_image.jpg')
                        st.image(image_url, width=150)
                    with col2:
                        st.subheader(anime.get('title', 'Título não disponível'))
                        st.write(anime.get('synopsis', 'Sinopse não disponível')[:200] + "...")
                        aired_date = anime.get('aired', {}).get('from', 'Data não disponível')
                        st.write(f"📅 Estreia: {aired_date[:10]}")
                        st.write(f"⭐ Nota: {anime.get('score', 'Sem nota')}")
                        st.link_button("Mais detalhes", anime.get('url', '#'))
        else:
            st.error("Não foi possível carregar a lista de animes.")
    else:
        st.warning("Faça login para ver os animes!")


