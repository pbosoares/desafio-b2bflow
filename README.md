# Desafio b2bflow — Estágio em Desenvolvimento Python

Script em Python que lê contatos cadastrados em uma tabela do Supabase e envia,
via Z-API, a mensagem personalizada:

> Olá, `<nome_contato>` tudo bem com você?

## 1. Setup da tabela no Supabase

No SQL Editor do seu projeto Supabase, rode:

```sql
create table contacts (
  id bigint generated always as identity primary key,
  nome_contato text not null,
  telefone text not null,   -- formato: DDI + DDD + número, ex: 5511999999999
  created_at timestamptz default now()
);
```

Para popular com até 3 contatos de teste:

```sql
insert into contacts (nome_contato, telefone) values
  ('Pablo', '5511999999999');
```

> O telefone deve estar sem espaços, traços ou parênteses (apenas dígitos),
> incluindo código do país (ex: 55 + DDD + número).

## 2. Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

```
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=sua-anon-ou-service-key
SUPABASE_TABLE=contacts
ZAPI_INSTANCE_ID=seu-instance-id
ZAPI_TOKEN=seu-token
ZAPI_CLIENT_TOKEN=seu-client-token   # se sua conta Z-API exigir
MAX_CONTACTS=3
```

- `SUPABASE_URL` e `SUPABASE_KEY`: em **Project Settings → API** no Supabase.
- `ZAPI_INSTANCE_ID` e `ZAPI_TOKEN`: no painel da sua instância Z-API
  (lembre de escanear o QR Code para conectar o WhatsApp).
- `ZAPI_CLIENT_TOKEN`: em **Segurança** no painel Z-API, se a opção
  "Token de Segurança da Conta" estiver ativada.

## 3. Como rodar

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
