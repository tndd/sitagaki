import pytest
from sqlmodel import SQLModel, create_engine

from infra.db.sqlmodel import SQLModelClient


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def test_sqlm_cli(test_engine):
    return SQLModelClient(test_engine)