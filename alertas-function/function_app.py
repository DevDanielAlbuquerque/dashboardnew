# Bibliotecas padrão do Python
from datetime import datetime, timedelta  # Manipulação de data e hora
import logging  # Registro de logs da execução
import os  # Leitura de variáveis de ambiente

# Bibliotecas de terceiros
import azure.functions as func  # Integração com Azure Functions
import pymssql  # Conexão com SQL Server
import requests  # Requisições HTTP para a API do Telegram

# Configuração da aplicação Azure Functions
app = func.FunctionApp()

# Função responsável por criar a conexão com o banco de dados
def conectar_sql():
    return pymssql.connect(
        server=os.getenv("DB_SERVER"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Função responsável por enviar mensagens para o Telegram
def enviar_telegram(mensagem):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logging.error("❌ TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não definidos")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": mensagem
    }

    try:
        response = requests.post(url, data=payload)
        logging.info(f"📡 Telegram status: {response.status_code}")
        logging.info(f"📡 Telegram resposta: {response.text}")
    except Exception as e:
        logging.error(f"❌ ERRO TELEGRAM: {str(e)}")


# Função principal executada por agendamento
@app.timer_trigger(schedule="0 0 11 * * *", arg_name="myTimer", run_on_startup=False)
def alerta_manha(myTimer: func.TimerRequest) -> None:
    logging.info("🚀 Executando alertas...")

    # Ajuste de horário para o fuso local utilizado pela regra
    agora = datetime.utcnow() - timedelta(hours=3)
    hoje = agora.date()
    hora = agora.hour

    # Regras de bloqueio para dias e horários fora da operação
    if agora.weekday() >= 5:
        logging.info("⛔ Final de semana - ignorando execução")
        return

    if hora < 8 or hora > 18:
        logging.info("⛔ Fora do horário comercial")
        return

    try:
        conn = conectar_sql()
        cursor = conn.cursor()
        logging.info("✅ Conectou no banco")

    except Exception as e:
        logging.error(f"❌ ERRO SQL: {str(e)}")
        return

    # Consulta dos alertas pendentes no banco
    cursor.execute("""
        SELECT id, descricao, data_vencimento, data_lembrete, data_ultimo_envio
        FROM alertas_dev
        WHERE status = 'PENDENTE'
    """)

    registros = cursor.fetchall()
    logging.info(f"📊 Registros encontrados: {len(registros)}")

    for row in registros:
        id_alerta = row[0]
        descricao = row[1]
        data_vencimento = row[2]
        data_lembrete = row[3]
        data_ultimo_envio = row[4]

        # Normalização das datas para facilitar comparações
        if hasattr(data_vencimento, "date"):
            data_vencimento = data_vencimento.date()

        if hasattr(data_lembrete, "date"):
            data_lembrete = data_lembrete.date()

        # Evita reenviar o mesmo alerta no mesmo dia
        if data_ultimo_envio:
            data_envio = data_ultimo_envio.date() if hasattr(data_ultimo_envio, "date") else data_ultimo_envio

            if data_envio == hoje:
                logging.info(f"⏭️ Já enviado hoje: {descricao}")
                continue

        # Verifica se o alerta já deve começar a ser enviado
        if hoje >= data_lembrete:
            dias_restantes = (data_vencimento - hoje).days

            if dias_restantes < 0:
                mensagem = f"🚨 ATRASADO!\n📌 {descricao}"
            elif dias_restantes == 0:
                mensagem = f"🚨 PRAZO FINAL HOJE\n📌 {descricao}"
            else:
                mensagem = f"📌 Lembrete\n{descricao}\n⏳ {dias_restantes} dias restantes"

            # Envio da mensagem para o Telegram
            enviar_telegram(mensagem)

            # Atualização da data do último envio no banco
            cursor.execute("""
                UPDATE alertas_dev
                SET data_ultimo_envio = GETDATE()
                WHERE id = %s
            """, (id_alerta,))

            conn.commit()
            logging.info(f"✅ Atualizado envio: {descricao}")

    conn.close()