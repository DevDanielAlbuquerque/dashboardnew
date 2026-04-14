from datetime import date
from typing import Tuple


def status_atrasado(data_vencimento: date, hoje: date) -> Tuple[str, str]:
    dias = abs((data_vencimento - hoje).days)
    return f"🔴 {dias} dias atrasado", "atrasado"


def status_proximo(data_vencimento: date, data_inicio: date, hoje: date) -> Tuple[str, str]:
    dias_restantes = (data_vencimento - hoje).days
    dias_para_inicio = (data_inicio - hoje).days

    if hoje < data_inicio:
        return f"🟢 Começa em {dias_para_inicio} dias", "futuro"
    if dias_restantes == 0:
        return "🟡 Hoje", "hoje"
    if 0 < dias_restantes <= 5:
        return f"⚠️ {dias_restantes} dias", "futuro"
    if dias_restantes > 5:
        return f"⏳ {dias_restantes} dias", "ok"
    return f"🔴 {abs(dias_restantes)} dias atrasado", "atrasado"