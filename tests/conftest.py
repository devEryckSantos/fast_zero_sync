import pytest  # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    # cria um banco de dados volátil em memória
    engine = create_engine('sqlite:///:memory:')

    # cria os metadados
    table_registry.metadata.create_all(engine)

    # gerenciamento de contexto,
    # cria a sessão utilizando o DB e retorna ele na função 'test_create_user'
    with Session(engine) as session:
        yield session

    # por fim, após o resultado do  teste
    # faça um tier donw: desfaça toda a operação
    table_registry.metadata.drop_all(engine)
