import streamlit as st

st.set_page_config(page_title="GeoSAB", page_icon="🌵", layout="centered")
st.sidebar.image("images/logo_geosab.webp")

st.title("🌵 GeoSAB – Por um Semiárido Produtivo e Sustentável")

st.markdown("""
O GeoSAB reune, organiza e disponibiliza **informações geográficas, ecológicas e agrícolas** sobre o **semiárido brasileiro**, com foco em práticas que apoiem o **desenvolvimento sustentável da região**.

Na presente versão você encontrará dados sobre:
- 🌿 Plantas **xerófitas** com potencial agrícola e ecológico
- 🌍 Mapeamento interativo dos **solos do semiárido** com delimitações:
    - Do semiárido
    - Da Caatinga
    - Dos Estados
    - E a descrições das principais classes de solo
- ✂️Vizualização e download de recortes dos solos por município 
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

# Rodapé com créditos atualizados
st.markdown(
    """
    <p style='text-align:center; font-size:14px;'>
        Projeto <strong>GeoSAB</strong> – Desenvolvido e mantido por <a href='https://daniloas.com' target='_blank'>daniloas.com</a>
        <br>
        Com o apoio da 
        <a href='https://codigoagro.com' target='_blank'>codigoagro.com</a> e 
        <a href='https://dadosagro.com' target='_blank'>dadosagro.com</a>
        
    </p>
    """,
    unsafe_allow_html=True
)
