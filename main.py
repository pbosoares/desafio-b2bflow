"""
Desafio b2bflow - Estágio em Desenvolvimento Python

Lê contatos cadastrados no Supabase e envia, via Z-API, a mensagem:
"Olá, <nome_contato> tudo bem com você?"

Uso:
    python main.py
"""

import os
import sys
import logging

import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "contacts")

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")  # opcional, exigido por algumas contas

MAX_CONTACTS = int(os.getenv("MAX_CONTACTS", "3"))

REQUIRED_VARS = {
    "SUPABASE_URL": SUPABASE_URL,
    "SUPABASE_KEY": SUPABASE_KEY,
    "ZAPI_INSTANCE_ID": ZAPI_INSTANCE_ID,
    "ZAPI_TOKEN": ZAPI_TOKEN,
}


def validate_env() -> None:
    """Garante que todas as variáveis de ambiente obrigatórias estão definidas."""
    missing = [name for name, value in REQUIRED_VARS.items() if not value]
    if missing:
        logger.error("Variáveis de ambiente faltando: %s", ", ".join(missing))
        logger.error("Confira o arquivo .env (veja .env.example).")
        sys.exit(1)


def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_contacts(client: Client, limit: int) -> list[dict]:
    """Busca até `limit` contatos na tabela configurada."""
    try:
        response = (
            client.table(SUPABASE_TABLE)
            .select("nome_contato, telefone")
            .limit(limit)
            .execute()
        )
    except Exception:
        logger.exception("Falha ao consultar a tabela '%s' no Supabase.", SUPABASE_TABLE)
        sys.exit(1)

    contacts = response.data or []
    if not contacts:
        logger.warning("Nenhum contato encontrado na tabela '%s'.", SUPABASE_TABLE)
    return contacts


def build_zapi_url() -> str:
    return f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"


def send_whatsapp_message(phone: str, message: str) -> bool:
    """Envia uma mensagem de texto via Z-API. Retorna True em caso de sucesso."""
    url = build_zapi_url()
    headers = {"Content-Type": "application/json"}
    if ZAPI_CLIENT_TOKEN:
        headers["Client-Token"] = ZAPI_CLIENT_TOKEN

    payload = {"phone": phone, "message": message}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        logger.info("Mensagem enviada para %s | resposta: %s", phone, resp.text)
        return True
    except requests.exceptions.RequestException:
        logger.exception("Falha ao enviar mensagem para %s", phone)
        return False


def main() -> None:
    validate_env()
    client = get_supabase_client()
    contacts = fetch_contacts(client, MAX_CONTACTS)

    if not contacts:
        logger.info("Encerrando: não há contatos para enviar mensagens.")
        return

    sent, failed = 0, 0
    for contact in contacts:
        nome = (contact.get("nome_contato") or "").strip()
        telefone = (contact.get("telefone") or "").strip()

        if not nome or not telefone:
            logger.warning("Contato inválido ignorado: %s", contact)
            failed += 1
            continue

        message = f"Olá, {nome} tudo bem com você?"
        if send_whatsapp_message(telefone, message):
            sent += 1
        else:
            failed += 1

    logger.info("Concluído. Enviadas: %d | Falhas: %d", sent, failed)


if __name__ == "__main__":
    main()
