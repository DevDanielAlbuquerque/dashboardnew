import streamlit as st

from telas.inicio import tela_inicio, carregar_css
from telas.dashboard import tela_dashboard
from telas.novo_alerta import tela_novo_alerta
from telas.editar_alerta import tela_editar_alerta

st.set_page_config(page_title="Central de Alertas", layout="wide")

# 👉 CSS global (melhor aqui)
carregar_css()

menu_opcoes = [
    "🏠 Início",
    "📊 Dashboard",
    "➕ Novo Alerta",
    "✏️ Editar"
]

if "menu" not in st.session_state:
    st.session_state["menu"] = "🏠 Início"

if st.session_state["menu"] not in menu_opcoes:
    st.session_state["menu"] = "📊 Dashboard"

menu = st.sidebar.radio(
    "Menu",
    menu_opcoes,
    index=menu_opcoes.index(st.session_state["menu"])
)

st.session_state["menu"] = menu

# ===== ROTAS =====

try:
    if menu == "🏠 Início":
        tela_inicio()

    elif menu == "📊 Dashboard":
        tela_dashboard()

    elif menu == "➕ Novo Alerta":
        tela_novo_alerta()

    elif menu == "✏️ Editar":
        tela_editar_alerta()

except Exception as e:
    st.error(f"Erro ao renderizar tela: {e}")