import pytest

from domain.materia.stock.bar.repository import BarRepository


@pytest.fixture
def test_bar_repo(test_peewee_cli):
    return BarRepository(test_peewee_cli)
