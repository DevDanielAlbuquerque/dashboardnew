import os
import streamlit as st


def carregar_css():
    """Carrega o arquivo CSS principal da aplicação Streamlit."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    caminho_css = os.path.join(base_dir, "styles", "style.css")

    try:
        with open(caminho_css, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao carregar CSS: {e}")