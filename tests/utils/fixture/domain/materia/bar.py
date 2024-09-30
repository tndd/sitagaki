import pytest

from domain.materia.finance.chart.repository import ChartRepository


@pytest.fixture
def test_chart_repo(test_peewee_cli):
    return ChartRepository(test_peewee_cli)
