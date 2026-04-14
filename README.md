# Alertas Azure

Projeto Python para gerenciamento e envio de alertas, com:

- **Frontend em Streamlit** para visualização e manutenção dos alertas
- **Backend em Azure Functions** para execução automática de notificações
- **SQL Server** como banco de dados
- **Telegram** como canal de envio das mensagens

---

## Estrutura do projeto

```text
alertasazure/
├── alertas-app/         # Frontend Streamlit
├── alertas-function/    # Backend Azure Functions
├── docs/                # Documentação do projeto
├── scripts/             # Scripts de execução local
├── shared/              # Constantes e utilitários compartilhados
└── README.md
```

---

## Objetivo

Centralizar o controle de alertas com cadastro, consulta, acompanhamento de prazos e envio automático de notificações.

---

## Componentes principais

### `alertas-app`
Aplicação web em Streamlit responsável por:

- listar alertas
- exibir indicadores
- cadastrar novos alertas
- editar alertas existentes

### `alertas-function`
Rotina automática responsável por:

- consultar alertas pendentes
- aplicar regras de envio
- enviar notificações para o Telegram
- registrar o último envio no banco

### `shared`
Espaço reservado para itens reutilizáveis entre frontend e backend, como:

- constantes
- utilitários
- funções auxiliares

---

## Como executar localmente

### Streamlit

```powershell
& "D:\Programacao\projetos\alertasazure\scripts\run_streamlit.ps1"
```

### Azure Functions

```powershell
& "D:\Programacao\projetos\alertasazure\scripts\run_function_local.ps1"
```

---

## Documentação adicional

Consultar a pasta `docs/`:

- `docs/arquitetura.md`
- `docs/fluxo-alertas.md`
- `docs/variaveis-de-ambiente.md`

---

## Status atual

O projeto está sendo reorganizado gradualmente com foco em:

- clareza
- organização
- baixo risco de mudança
- facilidade de estudo e manutenção