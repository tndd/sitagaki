import pytest

from domain.materia.finance.chart.repository import ChartRepository


@pytest.fixture
def test_chart_repo(test_peewee_cli, mock_get_barset_alpaca_api):
    """
    mock不使用の純粋なテスト用chatリポジトリ
    """
    yield ChartRepository(test_peewee_cli)


@pytest.fixture
def mock_test_chart_repo(test_peewee_cli, mock_get_barset_alpaca_api):
    """
    alpaca_apiの通信部分をモック化したchartリポジトリ
    """
    yield ChartRepository(test_peewee_cli)


@pytest.fixture
def mock_test_chart_repo_failed_api(test_peewee_cli, mock_get_barset_alpaca_api_empty_barset):
    """
    alpaca_apiの通信部分が必ず空を返すようにしたchartリポジトリ
    """
    yield ChartRepository(test_peewee_cli)