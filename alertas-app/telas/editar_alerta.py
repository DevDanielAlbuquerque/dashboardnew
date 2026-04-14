import streamlit as st

from services.database import (
    carregar_categorias,
    carregar_departamentos,
    conectar,
)


def tela_editar_alerta():
    """
    Renderiza a tela de edição de um alerta existente.
    """

    # ===== VALIDAÇÃO INICIAL =====
    # Garante que existe um alerta selecionado para edição.
    if "editar_id" not in st.session_state:
        st.warning("Nenhum alerta selecionado para edição.")
        return

    alerta_id = int(st.session_state["editar_id"])

    # ===== CABEÇALHO =====
    st.subheader("✏️ Editar Alerta")

    # ===== CARREGAMENTO DO ALERTA =====
    # Busca os dados atuais do alerta no banco para preencher o formulário.
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            departamento,
            categoria,
            descricao,
            observacoes,
            data_vencimento,
            data_lembrete
        FROM alertas_dev
        WHERE id = %s
    """, (alerta_id,))

    alerta = cursor.fetchone()
    conn.close()

    # Interrompe a tela caso o alerta não exista mais.
    if not alerta:
        st.error("Alerta não encontrado.")
        return

    (
        departamento_atual,
        categoria_atual,
        descricao_atual,
        observacao_atual,
        data_vencimento_atual,
        data_lembrete_atual,
    ) = alerta

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
        index=departamentos_opcoes.index(departamento_atual)
        if departamento_atual in departamentos_opcoes else 0
    )

    departamento = (
        st.text_input("Novo departamento", value=departamento_atual)
        if departamento_selecionado == "➕ Adicionar novo departamento"
        else departamento_selecionado
    )

    categoria_selecionada = st.selectbox(
        "Categoria",
        categorias_opcoes,
        index=categorias_opcoes.index(categoria_atual)
        if categoria_atual in categorias_opcoes else 0
    )

    categoria = (
        st.text_input("Nova categoria", value=categoria_atual)
        if categoria_selecionada == "➕ Adicionar nova categoria"
        else categoria_selecionada
    )

    descricao = st.text_input("Descrição", value=descricao_atual)
    observacao = st.text_area("Observação", value=observacao_atual)

    data_vencimento = st.date_input(
        "Data de vencimento",
        value=data_vencimento_atual,
    )

    data_lembrete = st.date_input(
        "Data de início do alerta",
        value=data_lembrete_atual,
    )

    # Exibe resumo visual das datas selecionadas.
    st.caption(f"📅 Vencimento: {data_vencimento.strftime('%d/%m/%Y')}")
    st.caption(f"🔔 Início do alerta: {data_lembrete.strftime('%d/%m/%Y')}")

    # ===== AÇÕES =====
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Salvar alterações"):
            # Valida campos obrigatórios antes de atualizar o registro.
            if not departamento or not categoria or not descricao:
                st.warning("Preencha os campos obrigatórios.")
                return

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE alertas_dev
                SET
                    departamento = %s,
                    categoria = %s,
                    descricao = %s,
                    observacoes = %s,
                    data_vencimento = %s,
                    data_lembrete = %s,
                    data_atualizacao = GETDATE()
                WHERE id = %s
            """, (
                departamento.strip(),
                categoria.strip(),
                descricao.strip(),
                observacao.strip() if observacao else "",
                data_vencimento,
                data_lembrete,
                alerta_id,
            ))

            conn.commit()
            conn.close()

            st.success("✅ Alerta atualizado com sucesso!")

            # Retorna para o dashboard após salvar.
            st.session_state["menu"] = "📊 Dashboard"
            st.session_state["selected_ids"] = []
            st.rerun()

    with col2:
        if st.button("⬅️ Cancelar"):
            # Retorna para o dashboard sem salvar alterações.
            st.session_state["menu"] = "📊 Dashboard"
            st.rerun()