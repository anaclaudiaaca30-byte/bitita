from fastapi.testclient import TestClient

from webapp.app.main import app

client = TestClient(app)


def test_list_students():
    response = client.get('/api/students')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_delete_student():
    payload = {
        'name': 'Maria Silva',
        'nationality': 'Brasileira',
        'generation': '1ª geração',
        'accommodation': 'Sim',
    }

    response = client.post('/api/students', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == payload['name']

    student_id = data['id']
    delete_response = client.delete(f'/api/students/{student_id}')
    assert delete_response.status_code == 204


def test_dashboard_endpoint():
    response = client.get('/api/dashboard')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
