import streamlit as st

from services.database import (
    carregar_categorias,
    carregar_departamentos,
    inserir_alerta,
)


def carregar_css():
    """
    Aplica estilos locais desta tela.
    """
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
        }

        section[data-testid="stSidebar"] {
            background-color: #161a23;
        }

        div[data-testid="stForm"] {
            background-color: #0e1117;
        }

        .block-container {
            padding-top: 2rem;
            background-color: #0e1117;
        }
        </style>
    """, unsafe_allow_html=True)


def tela_novo_alerta():
    """
    Renderiza a tela de criação de um novo alerta.
    """

    # ===== ESTILO LOCAL =====
    carregar_css()

    # ===== ESTADO INICIAL =====
    if "force_reset" not in st.session_state:
        st.session_state["force_reset"] = 0

    reset_key = st.session_state["force_reset"]

    # ===== CABEÇALHO =====
    st.subheader("➕ Criar novo alerta")

    # ===== DADOS AUXILIARES =====
    departamentos = carregar_departamentos()
    categorias = carregar_categorias()

    departamentos_opcoes = departamentos + ["➕ Adicionar novo departamento"]
    categorias_opcoes = categorias + ["➕ Adicionar nova categoria"]

    # ===== FORMULÁRIO =====
    departamento_selecionado = st.selectbox(
        "Departamento",
        departamentos_opcoes,
        key=f"departamento_sel_{reset_key}"
    )

    departamento = (
        st.text_input("Digite o novo departamento", key=f"novo_departamento_{reset_key}")
        if departamento_selecionado == "➕ Adicionar novo departamento"
        else departamento_selecionado
    )

    categoria_selecionada = st.selectbox(
        "Categoria",
        categorias_opcoes,
        key=f"categoria_sel_{reset_key}"
    )

    categoria = (
        st.text_input("Digite a nova categoria", key=f"nova_categoria_{reset_key}")
        if categoria_selecionada == "➕ Adicionar nova categoria"
        else categoria_selecionada
    )

    descricao = st.text_input("Descrição", key=f"descricao_{reset_key}")
    observacao = st.text_area("Observação", key=f"observacao_{reset_key}")

    data_vencimento = st.date_input(
        "Data do vencimento",
        format="DD/MM/YYYY",
        key=f"data_vencimento_{reset_key}"
    )

    data_lembrete = st.date_input(
        "Data do alerta começar a ser enviado",
        format="DD/MM/YYYY",
        key=f"data_lembrete_{reset_key}"
    )

    st.caption(f"📅 Vencimento: {data_vencimento.strftime('%d/%m/%Y')}")
    st.caption(f"🔔 Início do alerta: {data_lembrete.strftime('%d/%m/%Y')}")

    # ===== AÇÃO DE SALVAR =====
    if st.button("Salvar", key=f"salvar_{reset_key}"):

        # Validações
        if not departamento or not str(departamento).strip():
            st.warning("Preencha o Departamento.")
            return

        if not categoria or not str(categoria).strip():
            st.warning("Preencha a Categoria.")
            return

        if not descricao or not str(descricao).strip():
            st.warning("Preencha a Descrição.")
            return

        if data_lembrete > data_vencimento:
            st.warning("A data de início do alerta não pode ser maior que a data de vencimento.")
            return

        payload = {
            "departamento": departamento.strip(),
            "categoria": categoria.strip(),
            "descricao": descricao.strip(),
            "observacoes": observacao.strip() if observacao else "",
            "data_vencimento": data_vencimento.strftime("%Y-%m-%d"),
            "data_lembrete": data_lembrete.strftime("%Y-%m-%d"),
            "canal": "TELEGRAM",
            "status": "PENDENTE",
        }

        sucesso = inserir_alerta(payload)

        if not sucesso:
            st.error("Não foi possível salvar o alerta.")
            return

        st.session_state["force_reset"] += 1
        st.success("✅ Alerta salvo com sucesso!")

        st.session_state["menu"] = "📊 Dashboard"
        st.rerun()