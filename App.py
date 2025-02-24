from Api import get_animes
import streamlit as st


st.set_page_config(page_title= "Animes Atuais", layout= "wide")


st.markdown("<h1 style='text-align: center; font-family: Cursive; margin-bottom: 4rem'>📺 Animes da Temporada</h1>", unsafe_allow_html=True)

animes = get_animes()
for anime in animes:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(anime["images"]["jpg"]["image_url"], width=150)
    with col2:
        st.subheader(anime["title"])
        st.write(anime["synopsis"][:200] + "...")
        st.write(f"📅 Estreia: {anime['aired']['from'][0:10]}")
        st.write(f"⭐ Nota: {anime['score']}")
        st.link_button("Mais detalhes", anime["url"])