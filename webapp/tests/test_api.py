import pytest
from fastapi.testclient import TestClient

from webapp.app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def student_payload(**changes):
    payload = {
        "name": "Estudante fictício de teste",
        "nationality": "Brasil",
        "generation": "1ª geração",
        "accommodation": "Sim",
    }
    payload.update(changes)
    return payload


def test_homepage_exposes_accessible_controls_and_table(client):
    response = client.get("/")

    assert response.status_code == 200
    assert 'lang="pt-BR"' in response.text
    assert "Pular para o conteúdo principal" in response.text
    assert 'role="status"' in response.text
    assert '<caption class="sr-only">' in response.text
    assert '<th scope="col">' in response.text
    assert 'id="institutional_accommodation"' in response.text
    assert 'name="institutional_accommodation"' in response.text


def test_list_students(client):
    response = client.get("/api/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_existing_payload_defaults_to_not_informed(client):
    response = client.post(
        "/api/students",
        json=student_payload(),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["institutional_accommodation"] == "Não informado"

    saved = client.get("/api/students").json()
    student = next(item for item in saved if item["id"] == data["id"])
    assert student["institutional_accommodation"] == "Não informado"

    assert client.delete(
        f"/api/students/{data['id']}"
    ).status_code == 204


def test_create_update_and_delete_institutional_accommodation(client):
    response = client.post(
        "/api/students",
        json=student_payload(institutional_accommodation="Sim"),
    )

    assert response.status_code == 201
    data = response.json()
    student_id = data["id"]
    assert data["institutional_accommodation"] == "Sim"

    response = client.put(
        f"/api/students/{student_id}",
        json=student_payload(institutional_accommodation="Não"),
    )

    assert response.status_code == 200
    assert response.json()["institutional_accommodation"] == "Não"

    saved = client.get("/api/students").json()
    student = next(item for item in saved if item["id"] == student_id)
    assert student["institutional_accommodation"] == "Não"

    response = client.delete(f"/api/students/{student_id}")
    assert response.status_code == 204

    remaining = client.get("/api/students").json()
    assert all(item["id"] != student_id for item in remaining)


def test_rejects_invalid_institutional_accommodation(client):
    response = client.post(
        "/api/students",
        json=student_payload(
            institutional_accommodation="Valor inválido"
        ),
    )

    assert response.status_code == 422


def test_dashboard_endpoint(client):
    response = client.get("/api/dashboard")

    assert response.status_code == 200
    assert isinstance(response.json(), list)