import streamlit as st
from datetime import datetime


def render_header(nome_usuario: str = "Andressa") -> None:
    agora = datetime.now()
    hora = agora.hour

    if hora < 12:
        saudacao = "Bom dia"
    elif hora < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    st.markdown(
        f"""<div class="header-container">
<div>
<div class="header-title">📌 Central de Alertas</div>
<div class="header-subtitle">Gestão inteligente de prazos</div>
</div>
<div class="header-right">
<div class="header-greeting">{saudacao}, {nome_usuario} 👋</div>
<div class="header-datetime">{agora.strftime('%d/%m/%Y • %H:%M:%S')}</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )