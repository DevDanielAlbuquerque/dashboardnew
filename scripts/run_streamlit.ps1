# Define a raiz do projeto
$projectRoot = "D:\Programacao\projetos\alertasazure"

# Faz o Python enxergar a raiz do projeto, incluindo a pasta shared
$env:PYTHONPATH = $projectRoot

# Vai para a raiz do projeto
Set-Location $projectRoot

# Executa a aplicação Streamlit
streamlit run ".\alertas-app\app.py"