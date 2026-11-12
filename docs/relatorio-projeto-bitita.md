# Relatório do Projeto Bitita

**Data:** 12 de novembro de 2026  
**Projeto:** Sistema Web Bitita para cadastro e consulta de estudantes

## 1. Apresentação

O Bitita é um sistema para organizar informações de estudantes, com foco em cadastro, consulta e análise básica por nacionalidade. O repositório contém uma versão desktop em Python/Tkinter e uma aplicação web; este relatório descreve principalmente a aplicação web, desenvolvida com FastAPI.

## 2. Objetivo

Disponibilizar uma aplicação web que permita cadastrar, consultar, editar e excluir estudantes, apresentar os registros em uma tabela e resumir a quantidade de estudantes por nacionalidade em um dashboard.

## 3. Tecnologias utilizadas

| Área | Tecnologia ou recurso |
|---|---|
| Framework web e API | Python, FastAPI e Uvicorn |
| Interface | HTML, CSS e JavaScript |
| Templates | Jinja2 |
| Persistência e ORM | SQLAlchemy |
| Banco local | SQLite (`estudantes.db`) |
| Dados de demonstração | SQLite (`webapp/demo_estudantes.db`), com registros fictícios |
| Banco em nuvem preparado | PostgreSQL no Render (`bitita-db`) |
| Validação de dados | Pydantic |
| Testes | pytest e FastAPI TestClient |
| Controle de versão | Git |
| Análise de dados | Dashboard com contagem por nacionalidade |
| Contêiner e publicação | Dockerfile e instruções para Render |

## 4. Funcionalidades implementadas

- Cadastro de estudantes com nome, nacionalidade, geração e informação de acolhimento.
- Listagem dos estudantes em uma tabela e busca por nome.
- Edição e exclusão de registros.
- Confirmação antes de excluir um estudante.
- Dashboard que agrupa os registros por nacionalidade.
- API REST documentada automaticamente pelo FastAPI.
- Uso de SQLite durante o desenvolvimento local e suporte configurável a PostgreSQL por meio da variável `DATABASE_URL`.
- Compatibilidade da aplicação web com a tabela `estudantes` e os campos já usados pelo sistema desktop.

### Endpoints da API

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/api/students` | Listar estudantes |
| `POST` | `/api/students` | Cadastrar estudante |
| `PUT` | `/api/students/{student_id}` | Atualizar estudante |
| `DELETE` | `/api/students/{student_id}` | Excluir estudante |
| `GET` | `/api/dashboard` | Consultar totais por nacionalidade |

A documentação interativa da API fica disponível em `/docs` quando a aplicação está em execução.

## 5. Acessibilidade implementada

A interface inclui:

- Idioma da página definido como português do Brasil.
- Link para pular diretamente ao conteúdo principal.
- Rótulos associados aos campos e nome acessível para a busca.
- Destaque visível de foco para navegação por teclado.
- Cores de texto, botões e foco verificadas com contraste superior a 4,5:1 nos pares avaliados.
- Mensagens de status e alertas para leitores de tela.
- Indicação de carregamento e falhas ao buscar dados.
- Tabela com legenda acessível e cabeçalhos identificados por coluna.
- Botões de editar e excluir com nomes que identificam o estudante associado.
- Confirmação antes da exclusão.

Esses recursos formam uma base de acessibilidade; não representam, por si só, uma certificação de conformidade WCAG. Recomenda-se complementar com avaliação manual usando teclado, leitor de tela e ferramentas de auditoria.

## 6. Banco de dados e nuvem

O banco PostgreSQL `bitita-db` foi criado no Render. O código da aplicação aceita uma URL PostgreSQL definida em `DATABASE_URL`. Para desenvolvimento local, a configuração fica em `webapp/.env`; esse arquivo não deve ser enviado ao GitHub, pois contém credenciais.

**Estado da publicação:** o banco de dados está criado, mas a aplicação web ainda precisa ser publicada como um serviço Web Service separado no Render e configurada com a Internal Database URL. A URL do banco e outras credenciais não fazem parte deste relatório.

Os registros existentes no SQLite não são copiados automaticamente para o banco PostgreSQL. Caso seja necessário manter os dados atuais, será preciso planejar e executar uma migração.

Para compartilhamento seguro no GitHub, o repositório inclui uma base de demonstração separada, preenchida apenas com registros fictícios. Ela não é uma cópia dos dados pessoais da base local.

Após a publicação do site no Render, a plataforma fornece HTTPS para a URL pública. A configuração de produção e a verificação do endereço HTTPS ficam pendentes até o deploy do serviço web.

## 7. Controle de versão

O código está organizado em um repositório Git. As alterações do projeto podem ser acompanhadas por commits e enviadas ao GitHub para revisão e integração com o processo de deploy.

## 8. Testes realizados

Os testes automatizados verificam a página inicial e elementos acessíveis, a listagem de estudantes, a criação e exclusão de um registro e a resposta do dashboard.

Na execução realizada durante a preparação deste relatório, os testes da aplicação web terminaram com **4 aprovados**.

## 9. Próximas etapas

1. Criar e configurar o serviço Web Service do Bitita no Render, apontando para a pasta `webapp`.
2. Definir `DATABASE_URL` nas variáveis do serviço usando a Internal Database URL do banco `bitita-db`.
3. Executar o deploy e verificar a aplicação, os endpoints e a URL HTTPS pública.
4. Decidir se os dados locais devem ser migrados para o PostgreSQL.
5. Realizar testes manuais de acessibilidade com navegação por teclado e leitor de tela.

## 10. Conclusão

O Bitita Web atende aos principais componentes propostos para o projeto: framework web, banco de dados, JavaScript, API, recursos de acessibilidade, controle de versão, testes automatizados e análise básica de dados. A infraestrutura de PostgreSQL em nuvem já foi criada e a aplicação está preparada para configurá-la. Para concluir a entrega em nuvem, falta publicar o serviço web, configurar a conexão com o banco e validar o ambiente de produção.
