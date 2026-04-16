import os
import pandas as pd
import requests
import streamlit as st

from shared.constants import TABELA_ALERTAS


def _obter_configuracao(chave):
    """Obtém uma configuração do Streamlit secrets ou do ambiente."""
    try:
        valor = st.secrets.get(chave)
        if valor:
            return valor
    except Exception:
        pass

    return os.getenv(chave)


def _obter_api_url():
    api_url = _obter_configuracao("API_URL")

    if not api_url:
        st.error("Falta a configuração API_URL nos secrets do Streamlit.")
        return None

    return api_url.rstrip("/")


def _montar_headers():
    headers = {
        "Content-Type": "application/json"
    }

    api_key = _obter_configuracao("API_KEY")
    if api_key:
        headers["x-functions-key"] = api_key

    return headers


def listar_alertas():
    """
    Busca os alertas pela API e retorna um DataFrame.
    """
    api_url = _obter_api_url()
    if not api_url:
        return pd.DataFrame()

    try:
        response = requests.get(
            f"{api_url}/listar_alertas",
            headers=_montar_headers(),
            timeout=30
        )
        response.raise_for_status()

        dados = response.json()

        if isinstance(dados, list):
            return pd.DataFrame(dados)

        if isinstance(dados, dict):
            if "data" in dados and isinstance(dados["data"], list):
                return pd.DataFrame(dados["data"])
            return pd.DataFrame([dados])

        return pd.DataFrame()

    except Exception as e:
        st.error(f"Erro ao buscar alertas na API: {e}")
        return pd.DataFrame()


def inserir_alerta(alerta: dict) -> bool:
    """
    Envia um novo alerta para a API.
    """
    api_url = _obter_api_url()
    if not api_url:
        return False

    try:
        response = requests.post(
            f"{api_url}/criar_alerta",
            headers=_montar_headers(),
            json=alerta,
            timeout=30
        )
        response.raise_for_status()
        return True

    except Exception as e:
        st.error(f"Erro ao criar alerta via API: {e}")
        return False


def atualizar_alerta(alerta_id: int, dados_alerta: dict) -> bool:
    """
    Atualiza um alerta existente via API.
    """
    api_url = _obter_api_url()
    if not api_url:
        return False

    payload = {"id": alerta_id, **dados_alerta}

    try:
        response = requests.put(
            f"{api_url}/atualizar_alerta",
            headers=_montar_headers(),
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return True

    except Exception as e:
        st.error(f"Erro ao atualizar alerta via API: {e}")
        return False


def excluir_alerta(alerta_id: int) -> bool:
    """
    Exclui um alerta via API.
    """
    api_url = _obter_api_url()
    if not api_url:
        return False

    try:
        response = requests.delete(
            f"{api_url}/deletar_alerta?id={alerta_id}",
            headers=_montar_headers(),
            timeout=30
        )
        response.raise_for_status()
        return True

    except Exception as e:
        st.error(f"Erro ao excluir alerta via API: {e}")
        return False


def concluir_alerta(alerta_id: int) -> bool:
    """
    Marca um alerta como concluído via API.
    """
    api_url = _obter_api_url()
    if not api_url:
        return False

    try:
        response = requests.patch(
            f"{api_url}/concluir_alerta",
            headers=_montar_headers(),
            json={"id": alerta_id},
            timeout=30
        )
        response.raise_for_status()
        return True

    except Exception as e:
        st.error(f"Erro ao concluir alerta via API: {e}")
        return False


def carregar_alertas():
    """
    Mantém compatibilidade com código antigo que já chama essa função.
    """
    return listar_alertas()


def conectar():
    """
    Mantido apenas por compatibilidade com partes antigas do projeto.
    Não há mais conexão direta com o banco no Streamlit.
    """
    return None