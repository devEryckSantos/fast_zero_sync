from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação) -> literalmente o teste

    assert response.status_code == HTTPStatus.OK  # Assert
    assert (
        response.text
        == """
    <html>
      <head>
        <title> Nosso olá mundo! </title>
      </head>
      <body>
        <h1> Olá Mundo! </h1>
      </body>
    </html>"""
    )


def test_crate_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'eryck',
            'email': 'eryck@test.com',
            'password': 'password',
        },
    )
    # Validar se voltou o status code esperado (201)
    assert response.status_code == HTTPStatus.CREATED
    # Validar o UserPublic
    assert response.json() == {
        'username': 'eryck',
        'email': 'eryck@test.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    response_error = client.put(
        '/users/2',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }

    assert response_error.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1')
    response_error = client.delete('/users/2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}

    assert response_error.status_code == HTTPStatus.NOT_FOUND


def test_read_user_by_id(client):
    response = client.get('/users/1')
    response_error = client.get('/users/2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'eryck',
        'email': 'eryck@test.com',
        'id': 1,
    }
    assert response_error.status_code == HTTPStatus.NOT_FOUND
