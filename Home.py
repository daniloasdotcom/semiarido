import streamlit as st

st.set_page_config(
    page_title="Início - Semiárido Sustentável",
    page_icon="🌵",
    layout="wide"
)

st.title("🌵 GeoSAB – Semiárido Brasileiro Sustentável")

st.markdown("""
Este aplicativo tem como objetivo reunir, organizar e divulgar **informações geográficas, ecológicas e agrícolas** sobre o **semiárido brasileiro**, com foco em práticas que apoiem o **desenvolvimento sustentável da região**.

Aqui você encontrará dados sobre:
- 🌿 Plantas **xerófitas** com potencial agrícola e ecológico
- 🌍 Mapeamento interativo de **solos do semiárido**
- 📚 Base de dados em constante expansão
""")

st.divider()

st.subheader("🔍 Comece por aqui")
st.markdown("""
- [📍 **Solos do Semiárido**](./_Solos) — Explore o mapa interativo com diferentes camadas e simbologias.
- [🌿 **Xerófitas**](./_Xerofilas) — Consulte espécies adaptadas à seca, com informações de uso, origem e adaptabilidade.
""")

st.divider()

st.subheader("📢 Sobre o Projeto")
st.markdown("""
Este sistema foi idealizado para apoiar **pesquisadores, agricultores, estudantes e gestores públicos** interessados em promover o uso racional dos recursos naturais no semiárido, com base em informações acessíveis e organizadas.
""")

st.markdown("""
> “A sustentabilidade nasce do conhecimento aplicado ao território.”  
> — 🌎 Equipe GeoSAB
""")

st.divider()

# Rodapé com crédito
st.markdown(
    "<p style='text-align:center; font-size:14px;'>Projeto <strong>GeoSAB</strong> | Desenvolvido por <a href='https://daniloas.com' target='_blank'>daniloas.com</a></p>",
    unsafe_allow_html=True
)