# Bibliotecas de terceiros
import os  # Leitura de variaveis de ambiente como fallback seguro
import pandas as pd  # Manipulação de dados tabulares
import pymssql  # Conexão com SQL Server
import streamlit as st  # Acesso aos secrets e mensagens na interface

# Constantes compartilhadas do projeto
from shared.constants import TABELA_ALERTAS 


def _obter_configuracao(chave):
    """Obtém uma configuracao do Streamlit secrets ou do ambiente."""
    try:
        valor = st.secrets.get(chave)
        if valor:
            return valor
    except Exception:
        pass

    return os.getenv(chave)


def conectar():
    """
    Cria e retorna uma conexão com o banco de dados.

    Returns:
        pymssql.Connection | None: conexão ativa ou None em caso de erro.
    """
    servidor = _obter_configuracao("DB_SERVER")
    usuario = _obter_configuracao("DB_USER")
    senha = _obter_configuracao("DB_PASSWORD")
    banco = _obter_configuracao("DB_NAME")

    if not all([servidor, usuario, senha, banco]):
        st.error("Faltam variaveis de configuracao do banco de dados.")
        return None

    try:
        return pymssql.connect(
            server=servidor,
            user=usuario,
            password=senha,
            database=banco
        )
    except Exception as e:
        st.error(f"Erro na conexão com o banco: {e}")
        return None


def executar_consulta(query, mensagem_erro="Erro ao executar consulta"):
    """
    Executa uma consulta SQL e retorna o resultado em DataFrame.

    Args:
        query (str): instrução SQL a ser executada.
        mensagem_erro (str): mensagem exibida em caso de falha.

    Returns:
        pd.DataFrame: resultado da consulta ou DataFrame vazio.
    """
    conn = conectar()
    if conn is None:
        return pd.DataFrame()

    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"{mensagem_erro}: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def normalizar_colunas_de_data(df):
    """
    Converte colunas de data para datetime quando existirem no DataFrame.

    Args:
        df (pd.DataFrame): dados carregados do banco.

    Returns:
        pd.DataFrame: DataFrame com colunas de data normalizadas.
    """
    if "data_vencimento" in df.columns:
        df["data_vencimento"] = pd.to_datetime(df["data_vencimento"], errors="coerce")

    if "data_lembrete" in df.columns:
        df["data_lembrete"] = pd.to_datetime(df["data_lembrete"], errors="coerce")

    return df


def adicionar_status_visual(df):
    """
    Adiciona uma coluna visual com base na data de vencimento.

    Regras:
    - vencido: 🔴 Atrasado
    - vence hoje: 🟡 Hoje
    - demais casos: 🟢 No prazo

    Args:
        df (pd.DataFrame): DataFrame com a coluna data_vencimento.

    Returns:
        pd.DataFrame: DataFrame com a coluna status_visual.
    """
    if df.empty:
        return df

    hoje = pd.Timestamp.today().normalize()

    def calcular_status_visual(row):
        data_vencimento = row.get("data_vencimento")

        if pd.notna(data_vencimento):
            data_vencimento = data_vencimento.normalize()

            if data_vencimento < hoje:
                return "🔴 Atrasado"
            if data_vencimento == hoje:
                return "🟡 Hoje"

        return "🟢 No prazo"

    df["status_visual"] = df.apply(calcular_status_visual, axis=1)
    return df


def carregar_dados():
    """
    Carrega os alertas ainda não concluídos e aplica tratamentos básicos.

    Returns:
        pd.DataFrame: alertas carregados com datas tratadas e status visual.
    """
    query = f"""
        SELECT *
        FROM {TABELA_ALERTAS}
        WHERE status <> 'CONCLUIDO'
    """

    df = executar_consulta(query, "Erro ao carregar dados")

    if df.empty:
        return df

    df = normalizar_colunas_de_data(df)
    df = adicionar_status_visual(df)

    return df


def carregar_valores_distintos(nome_coluna):
    """
    Retorna valores distintos e não vazios de uma coluna da tabela principal.

    Args:
        nome_coluna (str): nome da coluna consultada.

    Returns:
        list: lista de valores distintos.
    """
    query = f"""
        SELECT DISTINCT {nome_coluna}
        FROM {TABELA_ALERTAS}
        WHERE {nome_coluna} IS NOT NULL
          AND LTRIM(RTRIM({nome_coluna})) <> ''
        ORDER BY {nome_coluna}
    """

    df = executar_consulta(
        query,
        f"Erro ao carregar valores da coluna '{nome_coluna}'"
    )

    if df.empty or nome_coluna not in df.columns:
        return []

    return df[nome_coluna].dropna().tolist()


def carregar_departamentos():
    """
    Carrega a lista de departamentos disponíveis.

    Returns:
        list: departamentos distintos e não vazios.
    """
    return carregar_valores_distintos("departamento")


def carregar_categorias():
    """
    Carrega a lista de categorias disponíveis.

    Returns:
        list: categorias distintas e não vazias.
    """
    return carregar_valores_distintos("categoria")