# Importa a biblioteca Streamlit e a apelida de "st" para uso mais curto no código.
import streamlit as st

# Importa a tela inicial e a função que carrega os estilos CSS personalizados.
from telas.inicio import tela_inicio, carregar_css

# Importa a função que renderiza a tela de dashboard.
from telas.dashboard import tela_dashboard

# Importa a função que renderiza o formulário de criação de novo alerta.
from telas.novo_alerta import tela_novo_alerta

# Importa a função que renderiza a tela de edição de alertas.
from telas.editar_alerta import tela_editar_alerta

# Configura a página do Streamlit com um título e layout em largura total.
st.set_page_config(page_title="Central de Alertas", layout="wide")

# ===== MENU =====
# Lista as opções exibidas no menu lateral.
menu_opcoes = [
    "🏠 Início",
    "📊 Dashboard",
    "➕ Novo Alerta",
    "✏️ Editar"
]

# Garante que a chave "menu" exista no estado da sessão.
if "menu" not in st.session_state:
    # Define a tela inicial padrão quando a aplicação abre.
    st.session_state["menu"] = "🏠 Início"

# Se o valor salvo no estado não existir mais na lista, reseta para uma opção válida.
if st.session_state["menu"] not in menu_opcoes:
    # Usa o dashboard como fallback seguro.
    st.session_state["menu"] = "📊 Dashboard"

# Cria o componente de rádio na barra lateral e guarda a opção selecionada.
menu = st.sidebar.radio(
    "Menu",
    menu_opcoes,
    # Usa o índice da opção salva no estado para manter a seleção ao recarregar.
    index=menu_opcoes.index(st.session_state["menu"])
)

# Atualiza o estado da sessão com a opção escolhida no menu.
st.session_state["menu"] = menu

# ===== ROTAS =====
# Se a opção selecionada for a tela inicial, executa a configuração e renderiza a página.
if menu == "🏠 Início":
    # Aplica os estilos CSS da interface.
    carregar_css()
    # Desenha o conteúdo da tela inicial.
    tela_inicio()

# Se a opção selecionada for o dashboard, renderiza essa tela.
elif menu == "📊 Dashboard":
    # Desenha o painel principal com indicadores e gráficos.
    tela_dashboard()

# Se a opção selecionada for a criação de alerta, abre o formulário correspondente.
elif menu == "➕ Novo Alerta":
    # Desenha a tela de cadastro de um novo alerta.
    tela_novo_alerta()

# Se a opção selecionada for edição, mostra a tela de edição de alertas.
elif menu == "✏️ Editar":
    # Desenha a tela para alterar alertas já existentes.
    tela_editar_alerta()