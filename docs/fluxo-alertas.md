# Fluxo de Alertas

## Objetivo

Descrever como os alertas são criados, consultados e enviados no sistema.

## Fluxo funcional

### 1. Cadastro do alerta
O alerta é criado pelo frontend Streamlit com informações como:
- descrição;
- departamento;
- categoria;
- data de vencimento;
- data de lembrete;
- status.

### 2. Armazenamento
Os dados são salvos na tabela principal do banco SQL Server.

### 3. Consulta no frontend
O Streamlit consulta os alertas no banco e apresenta:
- lista de alertas;
- indicadores;
- status visual;
- filtros por categoria, departamento e prazo.

### 4. Execução automática
A Azure Function é executada por agendamento.

### 5. Regras de envio
Durante a execução, o backend:
- verifica se está em dia útil;
- verifica se está dentro do horário permitido;
- consulta alertas pendentes;
- ignora alertas já enviados no mesmo dia;
- compara a data atual com a data de lembrete;
- calcula dias restantes para o vencimento.

### 6. Envio da notificação
Quando o alerta atende às regras, o backend envia uma mensagem para o Telegram.

### 7. Atualização do controle
Após o envio, o sistema registra a data do último envio no banco.

## Tipos de situação do alerta

- **Atrasado**: vencimento já passou.
- **Prazo final hoje**: vence no dia atual.
- **No prazo**: ainda possui dias restantes.

## Observações

Este fluxo está sendo melhorado gradualmente para aumentar:
- organização;
- robustez;
- clareza da estrutura;
- segurança no controle de envio.