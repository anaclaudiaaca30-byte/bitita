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

Use o Dockerfile para deploy em Render, Azure ou Railway.

## Controle de versão

```bash
git init
git add .
git commit -m "Primeiro commit"
```
