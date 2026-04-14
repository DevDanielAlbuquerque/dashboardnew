from datetime import datetime, timedelta


def normalizar_data(valor):
    """
    Converte datetime para date quando necessário.

    Args:
        valor: valor recebido do banco ou de outra camada.

    Returns:
        date | None: data normalizada ou o próprio valor, se já estiver no formato esperado.
    """
    if valor is None:
        return None

    return valor.date() if hasattr(valor, "date") else valor


def agora_brasil_utc_menos_3():
    """
    Retorna a data/hora atual considerando o ajuste manual UTC-3.

    Observação:
        Este ajuste mantém o comportamento atual do projeto.
        No futuro, pode ser substituído por tratamento explícito de timezone.
    """
    return datetime.utcnow() - timedelta(hours=3)