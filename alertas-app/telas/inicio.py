import streamlit as st
from datetime import datetime
import pandas as pd

from components.cards import render_alert_card
from components.header import render_header
from components.kpis import render_kpi
from services.database import carregar_dados
from utils.status import status_atrasado, status_proximo
from utils.style import carregar_css


def tela_inicio():
    """
    Renderiza a tela inicial com indicadores e listas de alertas.
    """
    carregar_css()
    render_header("Andressa")

    df = carregar_dados()

    if df.empty:
        st.info("Nenhum alerta encontrado.")
        return

    # Garante colunas esperadas
    colunas_esperadas = [
        "departamento",
        "descricao",
        "categoria",
        "data_vencimento",
        "data_lembrete",
    ]

    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            df[coluna] = None

    # Normaliza datas
    df["data_vencimento"] = pd.to_datetime(df["data_vencimento"], errors="coerce")
    df["data_lembrete"] = pd.to_datetime(df["data_lembrete"], errors="coerce")

    # Remove linhas sem data de vencimento válida
    df = df.dropna(subset=["data_vencimento"])

    if df.empty:
        st.info("Nenhum alerta com data válida encontrado.")
        return

    hoje = datetime.now().date()

    total = len(df)
    atrasados = len(df[df["data_vencimento"].dt.date < hoje])
    hoje_count = len(df[df["data_vencimento"].dt.date == hoje])
    proximos_7 = len(
        df[
            (df["data_vencimento"].dt.date >= hoje)
            & (df["data_vencimento"].dt.date <= hoje + pd.Timedelta(days=7))
        ]
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(render_kpi("Total", total), unsafe_allow_html=True)
    col2.markdown(render_kpi("7 dias", proximos_7), unsafe_allow_html=True)
    col3.markdown(render_kpi("Atrasados", atrasados), unsafe_allow_html=True)
    col4.markdown(render_kpi("Hoje", hoje_count), unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ===== ALERTAS ATRASADOS =====
    st.subheader("🔴 Atrasados")
    atrasados_df = (
        df[df["data_vencimento"].dt.date < hoje]
        .sort_values("data_vencimento")
        .head(6)
    )

    if atrasados_df.empty:
        st.caption("Nenhum atraso 🎉")
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(atrasados_df.iterrows()):
            col = cols[i % 3]
            status, classe = status_atrasado(row["data_vencimento"].date(), hoje)

            html = render_alert_card(
                departamento=row["departamento"] or "",
                descricao=row["descricao"] or "",
                categoria=row["categoria"] or "",
                data_vencimento=row["data_vencimento"],
                status=status,
                classe=classe,
            )
            col.markdown(html, unsafe_allow_html=True)

    # ===== PRÓXIMOS VENCIMENTOS =====
    st.subheader("⏳ Próximos vencimentos")
    proximos_df = (
        df[df["data_vencimento"].dt.date >= hoje]
        .sort_values("data_vencimento")
        .head(6)
    )

    if proximos_df.empty:
        st.caption("Nenhum alerta futuro.")
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(proximos_df.iterrows()):
            col = cols[i % 3]

            data_lembrete = row["data_lembrete"]
            if pd.isna(data_lembrete):
                data_lembrete = row["data_vencimento"]

            status, classe = status_proximo(
                row["data_vencimento"].date(),
                data_lembrete.date(),
                hoje,
            )

            html = render_alert_card(
                departamento=row["departamento"] or "",
                descricao=row["descricao"] or "",
                categoria=row["categoria"] or "",
                data_vencimento=row["data_vencimento"],
                data_inicio=data_lembrete,
                status=status,
                classe=classe,
            )
            col.markdown(html, unsafe_allow_html=True)