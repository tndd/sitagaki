import pytest

# @pytest.fixture
# def test_chart_repo(test_peewee_cli, replace_with_mock_get_barset_alpaca_api):
#     """
#     mock不使用の純粋なテスト用chatリポジトリ
#     """
#     yield ChartRepository(test_peewee_cli)


# @pytest.fixture
# def test_chart_repo_mocked_with_alpaca_api(test_peewee_cli, replace_with_mock_get_barset_alpaca_api):
#     """
#     alpaca_apiの通信部分をモック化したchartリポジトリ
#     """
#     yield ChartRepository(test_peewee_cli)


# @pytest.fixture
# def test_chart_repo_with_alpaca_api_fail_empty_barset(
#         test_peewee_cli,
#         replace_with_mock_get_barset_alpaca_api_fail_empty_barset
# ):
#     """
#     alpaca_apiの通信部分が必ず空を返すようにしたchartリポジトリ
#     """
#     yield ChartRepository(test_peewee_cli)
