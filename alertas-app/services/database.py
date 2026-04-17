import os
import pandas as pd
import requests
import streamlit as st


def _obter_configuracao(chave):
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
    headers = {"Content-Type": "application/json"}

    api_key = _obter_configuracao("API_KEY")
    if api_key:
        headers["x-functions-key"] = api_key

    return headers


def _normalizar_dataframe_alertas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante colunas mínimas e normaliza tipos para uso nas telas.
    """
    if df.empty:
        return df

    colunas_esperadas = [
        "id",
        "departamento",
        "categoria",
        "descricao",
        "observacoes",
        "data_vencimento",
        "data_lembrete",
        "status",
        "data_conclusao",
        "data_ultimo_envio",
        "canal",
    ]

    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            df[coluna] = None

    for coluna_data in [
        "data_vencimento",
        "data_lembrete",
        "data_conclusao",
        "data_ultimo_envio",
    ]:
        if coluna_data in df.columns:
            df[coluna_data] = pd.to_datetime(df[coluna_data], errors="coerce")

    return df


def listar_alertas():
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
            return _normalizar_dataframe_alertas(pd.DataFrame(dados))

        if isinstance(dados, dict):
            if "data" in dados and isinstance(dados["data"], list):
                return _normalizar_dataframe_alertas(pd.DataFrame(dados["data"]))
            return _normalizar_dataframe_alertas(pd.DataFrame([dados]))

        return pd.DataFrame()

    except requests.HTTPError as e:
        st.error(f"Erro HTTP ao buscar alertas: {e.response.status_code} - {e.response.text}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao buscar alertas na API: {e}")
        return pd.DataFrame()


def carregar_alertas():
    return listar_alertas()


def carregar_dados():
    """
    Mantém compatibilidade com telas antigas que chamam carregar_dados().
    """
    return listar_alertas()


def carregar_departamentos():
    """
    Deriva a lista de departamentos a partir dos alertas retornados pela API.
    Evita depender de rota específica no backend.
    """
    df = listar_alertas()

    if df.empty or "departamento" not in df.columns:
        return []

    departamentos = (
        df["departamento"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    departamentos = [d for d in departamentos.unique().tolist() if d]
    departamentos.sort()

    return departamentos


def carregar_categorias():
    """
    Deriva a lista de categorias a partir dos alertas retornados pela API.
    Evita depender de rota específica no backend.
    """
    df = listar_alertas()

    if df.empty or "categoria" not in df.columns:
        return []

    categorias = (
        df["categoria"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    categorias = [c for c in categorias.unique().tolist() if c]
    categorias.sort()

    return categorias


def inserir_alerta(alerta: dict) -> bool:
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
    except requests.HTTPError as e:
        st.error(f"Erro HTTP ao criar alerta: {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        st.error(f"Erro ao criar alerta via API: {e}")
        return False


def atualizar_alerta(alerta_id: int, dados_alerta: dict) -> bool:
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
    except requests.HTTPError as e:
        st.error(f"Erro HTTP ao atualizar alerta: {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        st.error(f"Erro ao atualizar alerta via API: {e}")
        return False


def excluir_alerta(alerta_id: int) -> bool:
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
    except requests.HTTPError as e:
        st.error(f"Erro HTTP ao excluir alerta: {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        st.error(f"Erro ao excluir alerta via API: {e}")
        return False


def concluir_alerta(alerta_id: int) -> bool:
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
    except requests.HTTPError as e:
        st.error(f"Erro HTTP ao concluir alerta: {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        st.error(f"Erro ao concluir alerta via API: {e}")
        return False


def conectar():
    """
    Mantido apenas por compatibilidade com partes antigas do projeto.
    O frontend não deve conectar direto no banco.
    """
    return None