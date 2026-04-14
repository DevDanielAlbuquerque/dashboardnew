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
    # Carrega os estilos globais da aplicação
    carregar_css()

    # Renderiza o cabeçalho principal da tela
    render_header("Andressa")

    # Carrega os dados dos alertas no banco
    df = carregar_dados()

    # Encerra a renderização caso não existam dados
    if df.empty:
        st.info("Nenhum alerta encontrado.")
        return

    # Define a data atual para cálculos de prazo
    hoje = datetime.now().date()

    # Calcula os principais indicadores da tela
    total = len(df)
    atrasados = len(df[df["data_vencimento"].dt.date < hoje])
    hoje_count = len(df[df["data_vencimento"].dt.date == hoje])
    proximos_7 = len(
        df[
            (df["data_vencimento"].dt.date >= hoje)
            & (df["data_vencimento"].dt.date <= hoje + pd.Timedelta(days=7))
        ]
    )

    # Exibe os KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(render_kpi("Total", total), unsafe_allow_html=True)
    col2.markdown(render_kpi("7 dias", proximos_7), unsafe_allow_html=True)
    col3.markdown(render_kpi("Atrasados", atrasados), unsafe_allow_html=True)
    col4.markdown(render_kpi("Hoje", hoje_count), unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Exibe a lista de alertas atrasados
    st.subheader("🔴 Atrasados")
    atrasados_df = df[df["data_vencimento"].dt.date < hoje].sort_values("data_vencimento").head(6)

    if atrasados_df.empty:
        st.caption("Nenhum atraso 🎉")
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(atrasados_df.iterrows()):
            col = cols[i % 3]
            status, classe = status_atrasado(row["data_vencimento"].date(), hoje)
            html = render_alert_card(
                departamento=row["departamento"],
                descricao=row["descricao"],
                categoria=row["categoria"],
                data_vencimento=row["data_vencimento"],
                status=status,
                classe=classe,
            )
            col.markdown(html, unsafe_allow_html=True)

    # Exibe a lista de alertas com vencimento próximo
    st.subheader("⏳ Próximos vencimentos")
    proximos_df = df[df["data_vencimento"].dt.date >= hoje].sort_values("data_vencimento").head(6)

    if proximos_df.empty:
        st.caption("Nenhum alerta futuro.")
    else:
        cols = st.columns(3)
        for i, (_, row) in enumerate(proximos_df.iterrows()):
            col = cols[i % 3]
            status, classe = status_proximo(
                row["data_vencimento"].date(),
                row["data_lembrete"].date(),
                hoje,
            )
            html = render_alert_card(
                departamento=row["departamento"],
                descricao=row["descricao"],
                categoria=row["categoria"],
                data_vencimento=row["data_vencimento"],
                data_inicio=row["data_lembrete"],
                status=status,
                classe=classe,
            )
            col.markdown(html, unsafe_allow_html=True)