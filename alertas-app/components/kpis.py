def render_kpi(title: str, value: int) -> str:
    return f"""<div class="card">
<div class="card-title">{title}</div>
<div class="card-value">{value}</div>
</div>"""