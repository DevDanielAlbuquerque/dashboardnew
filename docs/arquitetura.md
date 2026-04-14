# Arquitetura do Projeto

## Visão geral

Este projeto é dividido em duas partes principais:

- **Frontend (`alertas-app`)**: aplicação em Streamlit para visualização e gerenciamento dos alertas.
- **Backend (`alertas-function`)**: Azure Functions responsável por executar rotinas automáticas, como envio de alertas.
- **Banco de dados SQL Server**: armazena os alertas, datas, status e informações relacionadas.
- **Telegram**: canal usado para envio das notificações automáticas.

## Estrutura atual

```text
alertasazure/
├── alertas-app/
├── alertas-function/
├── docs/
├── scripts/
├── shared/
└── tests/
```

## Responsabilidades por módulo

### `alertas-app`
Responsável por:
- exibir alertas;
- cadastrar novos alertas;
- editar alertas existentes;
- apresentar indicadores e dashboards;
- aplicar estilos visuais com CSS.

### `alertas-function`
Responsável por:
- executar rotina agendada;
- consultar alertas pendentes;
- verificar regras de envio;
- enviar mensagens para o Telegram;
- atualizar controle de envio no banco.

### `shared`
Reservado para:
- constantes compartilhadas;
- utilitários comuns;
- funções reutilizáveis entre frontend e backend.

## Fluxo geral

1. O usuário cadastra ou edita alertas pelo Streamlit.
2. Os dados são armazenados no SQL Server.
3. A Azure Function executa em horário agendado.
4. O backend busca alertas pendentes.
5. Se o alerta estiver dentro da regra de envio, a mensagem é enviada ao Telegram.
6. O sistema registra a data do último envio.

## Objetivo da organização atual

A estrutura foi organizada para:
- melhorar clareza;
- facilitar estudo;
- reduzir acoplamento;
- permitir crescimento gradual do projeto.