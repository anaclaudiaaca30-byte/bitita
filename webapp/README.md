# Bitita Web

Aplicação web com FastAPI, SQLite, JavaScript, acessibilidade e análise de dados.

## Requisitos

- Python 3.11+
- Git

## Como rodar

```bash
cd webapp
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse:

- http://localhost:8000
- http://localhost:8000/docs

## Funcionalidades

- Cadastro de estudantes
- API REST
- Dashboard com contagem por nacionalidade
- Acessibilidade básica com labels e mensagens de status
- Testes automatizados com pytest
- Análise opcional com pandas

## Deploy em nuvem

O projeto já inclui suporte a container para deploy em Render ou Railway.

### Configuração recomendada

- Use o Dockerfile em `webapp/Dockerfile`
- Defina a variável `PORT=8000`
- Mantenha `DATABASE_URL` apontando para SQLite em ambiente de teste ou para um banco externo em produção
- O arquivo `railway.json` e `render.yaml` já foram preparados para uso rápido

### Exemplo de deploy no Render

1. Conecte o repositório ao Render.
2. Escolha "Web Service".
3. Configure o caminho do Dockerfile como `./webapp/Dockerfile`.
4. Use a pasta `./webapp` como contexto do build.
5. Acesse a URL pública gerada pelo Render.

### Exemplo de deploy no Railway

1. Conecte o repositório ao Railway.
2. O arquivo `railway.json` já aponta para o Dockerfile correto.
3. Faça o deploy e valide a saúde da aplicação em `/`.

### Variáveis de ambiente

```env
PORT=8000
APP_NAME=Bitita Web
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<database>
```

Se o deploy for apenas para testes locais, pode manter:

```env
DATABASE_URL=sqlite:///./bitita_web.db
```

> Para produção em nuvem, prefira um banco persistente como PostgreSQL (Render ou Railway oferecem esse suporte nativamente).

### Health check

A aplicação expõe o endpoint `/health` para checar se o serviço está vivo em produção.
Se o provedor fornecer uma URL começando com `postgres://`, a aplicação a converte para `postgresql://`.

## Controle de versão

```bash
git init
git add .
git commit -m "Primeiro commit"
```
