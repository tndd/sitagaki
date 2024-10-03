import pytest
from sqlalchemy import create_engine

from infra.db.alchemy.client import SQLAlchemyClient, SQLAlchemyModel


@pytest.fixture
def test_alchemy_cli():
    engine = create_engine('sqlite:///:memory:')
    SQLAlchemyModel.metadata.create_all(engine)
    cli = SQLAlchemyClient(engine)
    yield cli
    engine.dispose()
