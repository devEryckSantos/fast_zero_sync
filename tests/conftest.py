import pytest  # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    # cria um banco de dados volátil em memória
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # cria os metadados
    table_registry.metadata.create_all(engine)

    # gerenciamento de contexto,
    # cria a sessão utilizando o DB e retorna ele na função 'test_create_user'
    with Session(engine) as session:
        yield session

    # por fim, após o resultado do  teste
    # faça um tier donw: desfaça toda a operação
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    user = User(username='Teste', email='teste@test.com', password='testtest')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
