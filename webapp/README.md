# Bitita Web

Aplicação web com FastAPI, SQLite/PostgreSQL, JavaScript, acessibilidade e análise de dados.

## Requisitos

- Python 3.11+
- Git

## Como rodar

```bash
cd webapp
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Acesse:

- http://localhost:8000
- http://localhost:8000/docs

## Banco de dados na nuvem (Render)

1. Abra o banco `bitita-db` no painel do Render e copie a **External Database URL** em Connections.
2. Para rodar localmente, abra `webapp/.env` e defina `DATABASE_URL` com essa URL.
3. Para um serviço web hospedado no Render, abra o serviço, acesse Environment e adicione `DATABASE_URL` com a **Internal Database URL** do banco.
4. Reinicie o servidor ou faça um novo deploy. A aplicação aceita URLs PostgreSQL do Render; sem `DATABASE_URL`, continua usando o arquivo local `estudantes.db`.

Não publique nem compartilhe a URL do banco ou o arquivo `.env`: ambos dão acesso à senha. A configuração `.env` está ignorada pelo Git.

Os registros que já existem em `estudantes.db` não são copiados automaticamente para o Render. Faça uma importação dos dados antes de usar a base na nuvem se precisar manter os cadastros existentes.

## Banco de demonstração

O arquivo `demo_estudantes.db` contém somente registros fictícios, criado para demonstrações e para compartilhar o projeto sem publicar dados pessoais. Para iniciar a aplicação web com essa base no Windows:

```powershell
cd webapp
$env:DATABASE_URL = "sqlite:///./demo_estudantes.db"
uvicorn app.main:app --reload
```

O comando seleciona o banco apenas para essa sessão do terminal; a configuração padrão continua usando `estudantes.db`.

## Publicar a aplicação web no Render

O banco PostgreSQL e o site são serviços separados no Render. Para publicar o site:

1. Envie o repositório Bitita ao GitHub e, no Render, escolha **New > Web Service** para conectá-lo.
2. Selecione o repositório e configure **Root Directory** como `webapp` e **Runtime** como `Docker`. O Render usará o `webapp/Dockerfile`.
3. Em **Environment**, crie `DATABASE_URL` e informe a **Internal Database URL** do banco `bitita-db`.
4. Crie o serviço e aguarde o deploy. A URL pública fornecida pelo Render abrirá o sistema; acrescente `/docs` para acessar a documentação interativa da API.

Use a URL interna quando o site também estiver hospedado no Render. Para execução local, use a External Database URL em `webapp/.env`.

## Funcionalidades

- Cadastro de estudantes
- API REST
- Dashboard com contagem por nacionalidade
- Acessibilidade com link para pular ao conteúdo, foco visível, contraste reforçado, labels, mensagens de status, cabeçalhos de tabela e ações com nomes específicos para leitores de tela
- Testes automatizados com pytest
- Análise dos dados no dashboard por nacionalidade
- JavaScript para cadastro, edição, busca e exclusão via API

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
## Testes

Execute na raiz do repositório:

```bash
python -m pytest webapp/tests -q
```
