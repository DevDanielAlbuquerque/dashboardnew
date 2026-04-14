# ====================== telas/novo_alerta.py ======================

import streamlit as st

from services.database import (
    carregar_categorias,
    carregar_departamentos,
    conectar,
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
    # Aplica os estilos específicos desta tela.
    carregar_css()

    # ===== ESTADO INICIAL =====
    # Controla o reset dos campos após salvar um novo alerta.
    if "force_reset" not in st.session_state:
        st.session_state["force_reset"] = 0

    reset_key = st.session_state["force_reset"]

    # ===== CABEÇALHO =====
    st.subheader("➕ Criar novo alerta")

    # ===== DADOS AUXILIARES =====
    # Carrega listas usadas nos campos de seleção.
    departamentos = carregar_departamentos()
    categorias = carregar_categorias()

    departamentos_opcoes = departamentos + ["➕ Adicionar novo departamento"]
    categorias_opcoes = categorias + ["➕ Adicionar nova categoria"]

    # ===== FORMULÁRIO =====
    # Permite selecionar um valor existente ou informar um novo.
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

    # Exibe um resumo visual das datas informadas.
    st.caption(f"📅 Vencimento: {data_vencimento.strftime('%d/%m/%Y')}")
    st.caption(f"🔔 Início do alerta: {data_lembrete.strftime('%d/%m/%Y')}")

    # ===== AÇÃO DE SALVAR =====
    if st.button("Salvar", key=f"salvar_{reset_key}"):

        # Valida os campos obrigatórios antes de inserir no banco.
        if not departamento or not categoria or not descricao:
            st.warning("Preencha Departamento, Categoria e Descrição.")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO alertas_dev (
                departamento,
                categoria,
                descricao,
                observacoes,
                data_vencimento,
                data_lembrete,
                canal,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'TELEGRAM', 'PENDENTE')
        """, (
            departamento.strip(),
            categoria.strip(),
            descricao.strip(),
            observacao.strip() if observacao else "",
            data_vencimento,
            data_lembrete
        ))

        conn.commit()
        conn.close()

        # Reinicia os campos para a próxima abertura do formulário.
        st.session_state["force_reset"] += 1

        st.success("✅ Alerta salvo com sucesso!")

        # Retorna para o dashboard após o cadastro.
        st.session_state["menu"] = "📊 Dashboard"
        st.rerun()