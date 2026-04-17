import pandas as pd
import streamlit as st

from services.database import (
    atualizar_alerta,
    carregar_alertas,
    carregar_categorias,
    carregar_departamentos,
)


def tela_editar_alerta():
    """
    Renderiza a tela de edição de um alerta existente.
    """

    # ===== VALIDAÇÃO INICIAL =====
    if "editar_id" not in st.session_state:
        st.warning("Nenhum alerta selecionado para edição.")
        return

    alerta_id = int(st.session_state["editar_id"])

    # ===== CABEÇALHO =====
    st.subheader("✏️ Editar Alerta")

    # ===== CARREGAMENTO DO ALERTA =====
    df = carregar_alertas()

    if df.empty:
        st.error("Não foi possível carregar os alertas.")
        return

    if "id" not in df.columns:
        st.error("Os dados retornados não possuem a coluna 'id'.")
        return

    alerta_df = df[df["id"] == alerta_id]

    if alerta_df.empty:
        st.error("Alerta não encontrado.")
        return

    alerta = alerta_df.iloc[0]

    departamento_atual = str(alerta.get("departamento", "") or "")
    categoria_atual = str(alerta.get("categoria", "") or "")
    descricao_atual = str(alerta.get("descricao", "") or "")
    observacao_atual = str(alerta.get("observacoes", "") or "")

    data_vencimento_atual = pd.to_datetime(alerta.get("data_vencimento"), errors="coerce")
    data_lembrete_atual = pd.to_datetime(alerta.get("data_lembrete"), errors="coerce")

    if pd.isna(data_vencimento_atual):
        data_vencimento_atual = pd.Timestamp.today()

    if pd.isna(data_lembrete_atual):
        data_lembrete_atual = pd.Timestamp.today()

    # ===== DADOS AUXILIARES =====
    departamentos = carregar_departamentos()
    categorias = carregar_categorias()

    departamentos_opcoes = departamentos.copy()
    categorias_opcoes = categorias.copy()

    if departamento_atual and departamento_atual not in departamentos_opcoes:
        departamentos_opcoes.append(departamento_atual)

    if categoria_atual and categoria_atual not in categorias_opcoes:
        categorias_opcoes.append(categoria_atual)

    departamentos_opcoes = sorted(set([d for d in departamentos_opcoes if d]))
    categorias_opcoes = sorted(set([c for c in categorias_opcoes if c]))

    departamentos_opcoes += ["➕ Adicionar novo departamento"]
    categorias_opcoes += ["➕ Adicionar nova categoria"]

    # ===== FORMULÁRIO =====
    departamento_index = (
        departamentos_opcoes.index(departamento_atual)
        if departamento_atual in departamentos_opcoes else 0
    )

    departamento_selecionado = st.selectbox(
        "Departamento",
        departamentos_opcoes,
        index=departamento_index
    )

    departamento = (
        st.text_input("Novo departamento", value=departamento_atual)
        if departamento_selecionado == "➕ Adicionar novo departamento"
        else departamento_selecionado
    )

    categoria_index = (
        categorias_opcoes.index(categoria_atual)
        if categoria_atual in categorias_opcoes else 0
    )

    categoria_selecionada = st.selectbox(
        "Categoria",
        categorias_opcoes,
        index=categoria_index
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
        value=data_vencimento_atual.date(),
        format="DD/MM/YYYY",
    )

    data_lembrete = st.date_input(
        "Data de início do alerta",
        value=data_lembrete_atual.date(),
        format="DD/MM/YYYY",
    )

    st.caption(f"📅 Vencimento: {data_vencimento.strftime('%d/%m/%Y')}")
    st.caption(f"🔔 Início do alerta: {data_lembrete.strftime('%d/%m/%Y')}")

    # ===== AÇÕES =====
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Salvar alterações"):
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
            }

            sucesso = atualizar_alerta(alerta_id, payload)

            if not sucesso:
                st.error("Não foi possível atualizar o alerta.")
                return

            st.success("✅ Alerta atualizado com sucesso!")
            st.session_state["menu"] = "📊 Dashboard"
            st.session_state["selected_ids"] = []
            st.rerun()

    with col2:
        if st.button("⬅️ Cancelar"):
            st.session_state["menu"] = "📊 Dashboard"
            st.rerun()