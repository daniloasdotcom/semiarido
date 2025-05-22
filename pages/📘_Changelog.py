import streamlit as st

st.set_page_config(page_title="Changelog • GeoSAB", layout="centered")
st.sidebar.image("images/logo_geosab.webp")
st.sidebar.markdown("""
<div style='text-align: center; font-size: 1.2rem; margin-top: 0.5rem;'>
    Desenvolvido por<br><a href="https://daniloas.com" target="_blank" style="text-decoration: none;">daniloas.com</a>
</div>
""", unsafe_allow_html=True)

# Se estiver dentro da pasta changelog
with open("changelog/changelog.md", "r", encoding="utf-8") as f:
    changelog = f.read()

st.markdown(changelog)