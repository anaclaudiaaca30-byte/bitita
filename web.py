from flask import Flask

# Cria a aplicação Flask
app = Flask(__name__)


# Página inicial do Sistema Web Bitita
@app.route("/")
def inicio():
    return """
    <h1>Sistema Web Bitita</h1>

    <h2>Organização e Análise de Dados Escolares</h2>

    <p>
        Aplicação web destinada à organização, consulta
        e análise de dados escolares.
    </p>

    <h2>Problema identificado</h2>

    <p>
        A comunidade escolar apresentou dificuldade para
        organizar e consultar informações dos estudantes
        de forma integrada.
    </p>

    <h2>Necessidades identificadas</h2>

    <p>
        Organizar os dados escolares e facilitar a consulta
        das informações dos estudantes.
    </p>

    <p>
        Também será dada atenção às informações sobre
        nacionalidade e estudantes estrangeiros.
    </p>

    <h2>Status do projeto</h2>

    <p>
        Estrutura inicial da aplicação web criada com Flask.
    </p>
    """


# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
