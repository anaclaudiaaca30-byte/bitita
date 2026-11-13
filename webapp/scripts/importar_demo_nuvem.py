import json
import sqlite3
import unicodedata
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

API = "https://bitita.onrender.com/api/students"
ROOT = Path(__file__).resolve().parents[2]
DATABASE = ROOT / "estudantes.db"


def normalizar(valor):
    texto = " ".join(str(valor or "").split()).casefold()
    return "".join(
        letra
        for letra in unicodedata.normalize("NFD", texto)
        if unicodedata.category(letra) != "Mn"
    )


def sim_nao(valor, permitir_nao_informado=False):
    texto = normalizar(valor)

    if texto == "sim":
        return "Sim"
    if texto == "nao":
        return "Não"
    if permitir_nao_informado and texto in ("", "nao informado"):
        return "Não informado"

    raise ValueError(f"Valor de acolhimento desconhecido: {valor!r}")


def geracao(valor):
    texto = normalizar(valor)

    if texto in ("1", "1ª geração", "1a geracao", "1ª geracao"):
        return "1ª geração"
    if texto in ("2", "2ª geração", "2a geracao", "2ª geracao"):
        return "2ª geração"

    raise ValueError(f"Geração desconhecida: {valor!r}")


def requisicao(method="GET", payload=None):
    body = (
        json.dumps(payload, ensure_ascii=False).encode("utf-8")
        if payload is not None
        else None
    )
    request = Request(
        API,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(request, timeout=120) as response:
            return json.load(response)
    except HTTPError as error:
        detalhe = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API retornou {error.code}: {detalhe}") from error


def main():
    if not DATABASE.is_file():
        raise FileNotFoundError(f"Banco não encontrado: {DATABASE}")

    with sqlite3.connect(
        DATABASE.resolve().as_uri() + "?mode=ro", uri=True
    ) as connection:
        connection.row_factory = sqlite3.Row
        registros = connection.execute(
            "SELECT * FROM estudantes ORDER BY id"
        ).fetchall()

    # Valida todos os registros antes de enviar qualquer cadastro.
    payloads = []
    for registro in registros:
        payload = {
            "name": " ".join(registro["nome"].split()),
            "nationality": " ".join(registro["nacionalidade"].split()),
            "generation": geracao(registro["geracao"]),
            "accommodation": sim_nao(registro["acolhimento"]),
            "institutional_accommodation": sim_nao(
                registro["acolhimento_institucional"],
                permitir_nao_informado=True,
            ),
        }
        if not payload["name"] or not payload["nationality"]:
            raise ValueError(f"Cadastro incompleto no ID {registro['id']}")
        payloads.append(payload)

    existentes = requisicao()
    nomes_existentes = {
        normalizar(estudante["name"]) for estudante in existentes
    }

    criados = 0
    ignorados = 0

    for payload in payloads:
        chave = normalizar(payload["name"])

        # Nesta demonstração, um nome já existente não será reenviado.
        if chave in nomes_existentes:
            print(f"Já existe, não reenviado: {payload['name']}")
            ignorados += 1
            continue

        requisicao("POST", payload)
        nomes_existentes.add(chave)
        criados += 1
        print(f"Cadastrado: {payload['name']}")

    print(f"\nConcluído: {criados} criados; {ignorados} não reenviados.")
    print("O banco local foi apenas consultado.")


if __name__ == "__main__":
    main()