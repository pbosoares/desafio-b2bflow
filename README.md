# Desafio b2bflow — Estágio em Desenvolvimento Python

Script em Python que lê contatos cadastrados em uma tabela do Supabase e envia,
via Z-API, a mensagem personalizada:

> Olá, `<nome_contato>` tudo bem com você?

Envia para até 3 contatos (ou menos, se a tabela tiver menos registros).

## Tecnologias

- Python 3.10+
- [Supabase](https://supabase.com) (plano free) — banco de dados
- [Z-API](https://www.z-api.io) (plano free) — envio de WhatsApp

## 1. Setup da tabela no Supabase

No SQL Editor do seu projeto Supabase, rode:

```sql
create table contacts (
  id bigint generated always as identity primary key,
  nome_contato text not null,
  telefone text not null,   -- formato: DDI + DDD + número, ex: 5511999999999
  created_at timestamptz default now()
);

insert into contacts (nome_contato, telefone) values
  ('Marcelo', '5511999999999'),
  ('Ana', '5521988888888'),
  ('João', '5531977777777');
```

> O telefone deve estar sem espaços, traços ou parênteses (apenas dígitos),
> incluindo código do país.

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

- `SUPABASE_URL` e `SUPABASE_KEY`: encontrados em **Project Settings → API** no Supabase.
- `ZAPI_INSTANCE_ID` e `ZAPI_TOKEN`: encontrados no painel da sua instância Z-API
  (lembre de escanear o QR Code para conectar o WhatsApp).
- `ZAPI_CLIENT_TOKEN`: aparece em **Segurança** no painel Z-API, se a opção
  "Token de Segurança da Conta" estiver ativada.

## 3. Instalação

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Como rodar

```bash
python main.py
```

O script vai:
1. Validar se todas as variáveis de ambiente necessárias estão definidas.
2. Buscar até `MAX_CONTACTS` contatos na tabela do Supabase.
3. Enviar a mensagem personalizada para cada um via Z-API.
4. Logar no terminal sucesso/falha de cada envio e um resumo final.

## Estrutura do projeto

```
.
├── main.py            # script principal
├── requirements.txt   # dependências
├── .env.example        # modelo de variáveis de ambiente
├── .gitignore
└── README.md
```

## Tratamento de erros

- Variáveis de ambiente ausentes interrompem a execução com log claro.
- Falhas de conexão com Supabase ou Z-API são logadas com `logger.exception`
  (stack trace completo) sem derrubar o restante do processo, exceto quando
  a configuração básica está incorreta.
- Contatos com nome ou telefone vazios são ignorados e contabilizados como falha.
