# Variáveis de Ambiente

## Objetivo

Documentar as variáveis usadas pelo projeto no frontend e no backend.

---

## Banco de dados

Usadas para conexão com o SQL Server:

- `DB_SERVER`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

### Descrição

- **DB_SERVER**: endereço do servidor SQL Server.
- **DB_USER**: usuário de acesso ao banco.
- **DB_PASSWORD**: senha do usuário.
- **DB_NAME**: nome do banco de dados.

---

## Telegram

Usadas para envio de mensagens:

- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`

### Descrição

- **TELEGRAM_TOKEN**: token do bot do Telegram.
- **TELEGRAM_CHAT_ID**: identificador do chat ou grupo que receberá as mensagens.

---

## Onde são usadas

### `alertas-app`
No frontend Streamlit, as configurações podem vir de:
- `st.secrets`
- ambiente local configurado conforme a aplicação

### `alertas-function`
No backend Azure Functions, as variáveis são lidas com:
- `os.getenv(...)`

Podem estar em:
- `local.settings.json` no ambiente local
- configurações da Function App no Azure

## Arquivos de exemplo seguros

Para manter o repositório limpo, o projeto agora inclui modelos sem segredos reais:

- [`.env.example`](../.env.example)
- [`alertas-app/.streamlit/secrets.toml.example`](../alertas-app/.streamlit/secrets.toml.example)
- [`alertas-function/local.settings.json.example`](../alertas-function/local.settings.json.example)

Use esses arquivos como base para criar os arquivos locais reais, que continuam fora do GitHub.

---

## Exemplo de uso no backend

```python
token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
```

## Exemplo de uso no frontend

```python
server = st.secrets["DB_SERVER"]
```

---

## Boas práticas

- não versionar senhas e tokens no repositório;
- manter credenciais fora do código-fonte;
- usar nomes consistentes entre ambientes;
- documentar qualquer nova variável adicionada ao projeto.