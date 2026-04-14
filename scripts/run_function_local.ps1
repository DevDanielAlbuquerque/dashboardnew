# Define a raiz do projeto
$projectRoot = "D:\Programacao\projetos\alertasazure"

# Define a pasta da Azure Function
$functionPath = Join-Path $projectRoot "alertas-function"

# Faz o Python enxergar a raiz do projeto, incluindo a pasta shared
$env:PYTHONPATH = $projectRoot

# Vai para a pasta da Function
Set-Location $functionPath

# Inicia a Azure Function localmente
func start