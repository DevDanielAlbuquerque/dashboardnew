# ====================== telas/dashboard.py ======================

import pandas as pd
import streamlit as st

from services.database import (
    carregar_categorias,
    carregar_dados,
    carregar_departamentos,
    conectar,
)


def tela_dashboard():
    """
    Renderiza a tela de dashboard com filtros, ações e listagem de alertas.
    """

    # ===== ESTADO INICIAL =====
    # Inicializa chaves usadas pela tela para evitar erros de Session State.
    if "reset_filtros" not in st.session_state:
        st.session_state["reset_filtros"] = False

    if "page" not in st.session_state:
        st.session_state["page"] = 1

    if "selected_ids" not in st.session_state:
        st.session_state["selected_ids"] = []

    if "selecionados_map" not in st.session_state:
        st.session_state["selecionados_map"] = {}

    if "confirm_concluir" not in st.session_state:
        st.session_state["confirm_concluir"] = False

    if "confirm_delete" not in st.session_state:
        st.session_state["confirm_delete"] = False

    if "pesquisar" not in st.session_state:
        st.session_state["pesquisar"] = False

    if "menu" not in st.session_state:
        st.session_state["menu"] = "📊 Dashboard"

    # ===== CARREGAMENTO INICIAL =====
    # Busca os dados e listas usadas pelos filtros.
    df = carregar_dados()
    departamentos = carregar_departamentos()
    categorias = carregar_categorias()

    # Interrompe a renderização caso não existam dados.
    if df.empty:
        st.info("Nenhum dado encontrado para exibir no dashboard.")
        return

    # ===== FILTROS =====
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        departamento = st.selectbox(
            "Departamento",
            ["Todos"] + departamentos,
            key=f"f_departamento_{st.session_state['reset_filtros']}"
        )

    with col2:
        categoria = st.selectbox(
            "Categoria",
            ["Todos"] + categorias,
            key=f"f_categoria_{st.session_state['reset_filtros']}"
        )

    with col3:
        status = st.selectbox(
            "Status",
            ["Todos", "PENDENTE", "CONCLUIDO"],
            key=f"f_status_{st.session_state['reset_filtros']}"
        )

    with col4:
        descricao = st.text_input(
            "Descrição",
            key=f"f_descricao_{st.session_state['reset_filtros']}"
        )

    col5, col6 = st.columns(2)

    with col5:
        Data_inicio = st.date_input(
            "Data vencimento início",
            value=None,
            format="DD/MM/YYYY",
            key=f"f_data_inicio_{st.session_state['reset_filtros']}"
        )

    with col6:
        data_fim = st.date_input(
            "Data vencimento fim",
            value=None,
            format="DD/MM/YYYY",
            key=f"f_data_fim_{st.session_state['reset_filtros']}"
        )

    # ===== BOTÕES =====
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("➕ Novo Alerta"):
            st.session_state["menu"] = "➕ Novo Alerta"
            st.rerun()

    with col_btn2:
        if st.button("🔍 Pesquisar"):
            st.session_state["pesquisar"] = True
            st.session_state["page"] = 1
            st.session_state["selected_ids"] = []

    with col_btn3:
        if st.button("🧹 Limpar Filtros"):
            st.session_state["reset_filtros"] = not st.session_state["reset_filtros"]
            st.session_state["pesquisar"] = False
            st.session_state["page"] = 1
            st.session_state["selected_ids"] = []
            st.session_state["selecionados_map"] = {}
            st.rerun()

    st.markdown("---")

    # ===== CABEÇALHO E AÇÕES =====
    col_titulo, col_acoes = st.columns([6, 4])

    with col_titulo:
        st.subheader("📋 Lista de Alertas")

    with col_acoes:
        selected = st.session_state["selected_ids"]
        disabled = len(selected) == 0
        only_one = len(selected) == 1

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✔️", disabled=disabled, help="Concluir"):
                st.session_state["confirm_concluir"] = True

        with col2:
            if st.button("✏️", disabled=not only_one, help="Editar"):
                st.session_state["editar_id"] = int(selected[0])
                st.session_state["menu"] = "✏️ Editar"
                st.rerun()

        with col3:
            if st.button("🗑️", disabled=disabled, help="Excluir"):
                st.session_state["confirm_delete"] = True

    # ===== CONFIRMAÇÃO DE CONCLUSÃO =====
    if st.session_state["confirm_concluir"]:
        st.warning("⚠️ Deseja realmente concluir os alertas selecionados?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Sim concluir"):
                conn = conectar()
                cursor = conn.cursor()

                for alerta_id in st.session_state["selected_ids"]:
                    cursor.execute(
                        "UPDATE alertas_dev SET status='CONCLUIDO', data_conclusao=GETDATE() WHERE id=%s",
                        (int(alerta_id),)
                    )

                conn.commit()
                conn.close()

                st.session_state["selected_ids"] = []
                st.session_state["confirm_concluir"] = False
                st.success("Alertas concluídos!")
                st.rerun()

        with col2:
            if st.button("❌ Cancelar"):
                st.session_state["confirm_concluir"] = False

    # ===== CONFIRMAÇÃO DE EXCLUSÃO =====
    if st.session_state["confirm_delete"]:
        st.warning("⚠️ Tem certeza que deseja excluir os alertas?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Sim excluir"):
                conn = conectar()
                cursor = conn.cursor()

                for alerta_id in st.session_state["selected_ids"]:
                    cursor.execute(
                        "DELETE FROM alertas_dev WHERE id=%s",
                        (int(alerta_id),)
                    )

                conn.commit()
                conn.close()

                st.session_state["selected_ids"] = []
                st.session_state["confirm_delete"] = False
                st.success("Alertas excluídos!")
                st.rerun()

        with col2:
            if st.button("❌ Cancelar"):
                st.session_state["confirm_delete"] = False

    # ===== CONTROLE DE PESQUISA =====
    if not st.session_state["pesquisar"]:
        st.info("Clique em pesquisar para visualizar os dados")
        return

    # ===== FILTRAGEM DOS DADOS =====
    df = carregar_dados()

    if departamento != "Todos":
        df = df[df["departamento"] == departamento]

    if categoria != "Todos":
        df = df[df["categoria"] == categoria]

    if status != "Todos":
        df = df[df["status"] == status]

    if descricao:
        df = df[df["descricao"].str.contains(descricao, case=False, na=False)]

    if data_inicio:
        df = df[df["data_vencimento"] >= pd.to_datetime(data_inicio)]

    if data_fim:
        df = df[df["data_vencimento"] <= pd.to_datetime(data_fim)]

    if df.empty:
        st.warning("Nenhum resultado encontrado")
        return

    # ===== PAGINAÇÃO =====
    page_size = 10
    total_rows = len(df)
    total_pages = max((total_rows - 1) // page_size + 1, 1)

    if st.session_state["page"] > total_pages:
        st.session_state["page"] = total_pages

    start = (st.session_state["page"] - 1) * page_size
    end = start + page_size

    df_page = df.iloc[start:end].copy()

    # Formata apenas a copia usada na exibicao, preservando o DataFrame original para filtros e acoes.
    for coluna_data in ["data_vencimento", "data_lembrete", "data_conclusao", "data_ultimo_envio"]:
        if coluna_data in df_page.columns:
            df_page[coluna_data] = pd.to_datetime(df_page[coluna_data], errors="coerce").dt.strftime("%d/%m/%Y")

    # ===== SELEÇÃO DE LINHAS =====
    df_page["Selecionar"] = df_page["id"].map(
        lambda x: st.session_state["selecionados_map"].get(x, False)
    )

    edited_df = st.data_editor(
        df_page,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": None,
            "canal": None,
        }
    )

    # Atualiza o mapa de seleção com base na edição da tabela.
    for _, row in edited_df.iterrows():
        st.session_state["selecionados_map"][row["id"]] = row["Selecionar"]

    # Atualiza a lista consolidada de IDs selecionados.
    st.session_state["selected_ids"] = [
        id_
        for id_, selected in st.session_state["selecionados_map"].items()
        if selected
    ]

    # ===== CONTROLES DE PAGINAÇÃO =====
    colp1, colp2, colp3 = st.columns([1, 2, 1])

    with colp1:
        if st.button("⬅️ Anterior"):
            if st.session_state["page"] > 1:
                st.session_state["page"] -= 1
                st.session_state["selected_ids"] = []
                st.rerun()

    with colp2:
        st.markdown(
            f"<div style='text-align:center'>Página {st.session_state['page']} de {total_pages}</div>",
            unsafe_allow_html=True
        )

    with colp3:
        if st.button("Próxima ➡️"):
            if st.session_state["page"] < total_pages:
                st.session_state["page"] += 1
                st.session_state["selected_ids"] = []
                st.rerun()

    st.markdown("---")