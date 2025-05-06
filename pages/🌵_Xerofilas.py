import streamlit as st
from plant_datum.plant_database import criar_tabela, adicionar_planta, listar_plantas, buscar_por_nome
from plant_datum.initial_data import dados_iniciais

# ---------------------
# CONFIGURAÇÃO
# ---------------------

st.set_page_config(page_title="Xerófitas do Semiárido", page_icon="🌵")
st.title("🌵 Banco de Dados de Xerófitas - Semiárido Brasileiro")

# Inicializa banco e dados básicos
criar_tabela()
dados_iniciais()

# ---------------------
# CONTROLE DE ACESSO
# ---------------------

DESENVOLVEDOR = "danilo"
SENHA = "1234"  # Altere conforme preferir

modo = st.sidebar.selectbox("Modo de acesso", ["Usuário", "Desenvolvedor"])
acesso_autorizado = False

if modo == "Desenvolvedor":
    senha = st.sidebar.text_input("Senha", type="password")
    if senha == SENHA:
        acesso_autorizado = True
    else:
        st.sidebar.warning("Senha incorreta.")

# ---------------------
# MENU CONDICIONAL
# ---------------------

if acesso_autorizado:
    menu = st.sidebar.selectbox("Menu", ["Adicionar Nova Planta", "Buscar Planta"])
else:
    menu = "Buscar Planta"

# ---------------------
# ADICIONAR PLANTA (desenvolvedor)
# ---------------------

if menu == "Adicionar Nova Planta" and acesso_autorizado:
    st.subheader("🌱 Adicionar Nova Planta")

    nome_cientifico = st.text_input("Nome científico")
    nome_popular = st.text_input("Nome popular")
    origem = st.text_input("Origem")
    uso = st.text_area("Uso")
    caracteristicas = st.text_area("Características adaptativas")
    observacoes = st.text_area("Observações")

    if st.button("Salvar"):
        if nome_cientifico and nome_popular:
            adicionar_planta(nome_cientifico, nome_popular, origem, uso, caracteristicas, observacoes)
            st.success("✅ Planta adicionada com sucesso!")
        else:
            st.warning("Preencha ao menos o nome científico e o nome popular.")

# ---------------------
# BUSCAR PLANTA (todos)
# ---------------------

elif menu == "Buscar Planta":
    st.subheader("🔎 Buscar Planta por Nome Popular")

    plantas = listar_plantas()

    if plantas:
        nomes_populares = [p[2] for p in plantas]
        opcao = st.selectbox("Selecione uma planta:", nomes_populares)

        if opcao:
            planta = next(p for p in plantas if p[2] == opcao)

            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color: rgba(240, 240, 240, 0.05); 
                        padding: 1rem; 
                        border-radius: 0.75rem; 
                        border: 1px solid rgba(150,150,150,0.2);
                    ">
                        <p style="font-size:16px;"><strong>🌿 Nome popular:</strong> {planta[2]}</p>
                        <p style="font-size:15px;"><strong>🔬 Nome científico:</strong> <em>{planta[1]}</em></p>
                        <p style="font-size:15px;"><strong>🌍 Origem:</strong> {planta[3]}</p>
                        <p style="font-size:15px;"><strong>🍽️ Uso:</strong> {planta[4]}</p>
                        <p style="font-size:15px;"><strong>💧 Características adaptativas:</strong> {planta[5]}</p>
                        <p style="font-size:15px;"><strong>📝 Observações:</strong> {planta[6]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("Nenhuma planta cadastrada ainda.")