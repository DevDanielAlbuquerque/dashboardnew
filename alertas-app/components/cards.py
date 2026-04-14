import pandas as pd
from datetime import datetime

def render_alert_card(
    departamento: str,
    descricao: str,
    categoria: str,
    data_vencimento: datetime,
    status: str,
    classe: str,
    data_inicio: datetime | None = None,
) -> str:

    inicio_html = ""

    if data_inicio is not None:
        inicio_html = f"""<div class="alert-date">⏰ Início: {data_inicio.strftime("%d/%m/%Y")}</div>"""

    return f"""<div class="alert-card {classe}">
<div class="alert-departamento">🏢 {departamento}</div>
<div class="alert-title">{descricao}</div>
<div class="alert-category">📁 {categoria}</div>
<div class="alert-date">📅 {data_vencimento.strftime("%d/%m/%Y")}</div>
{inicio_html}
<div class="alert-warning">{status}</div>
</div>"""