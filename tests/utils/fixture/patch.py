import pytest
from alpaca.data.models import BarSet

from tests.utils.mock.infra.api.alpaca.bar import generate_barset_alpaca

MODULE_PATH_GET_BARSET_ALPACA_API = 'infra.api.alpaca.bar.get_barset_alpaca_api'


@pytest.fixture
def patch_with_mock_get_barset_alpaca_api(monkeypatch):
    """
    通信をモックし、ダミーのBarSetを返す。
    """
    def _mock_get_barset_alpaca_api(*args, **kwargs):
        return generate_barset_alpaca()

    monkeypatch.setattr(
        MODULE_PATH_GET_BARSET_ALPACA_API,
        _mock_get_barset_alpaca_api
    )


@pytest.fixture
def patch_with_mock_get_barset_alpaca_api_fail_empty_barset(monkeypatch):
    """
    空のBarSetを返す。
    ただし空のBarSetという戻り値はあり得ることなのでエラーではない。
    そのためerrではなくfailとしている。
    """
    def _mock_get_barset_alpaca_api(*args, **kwargs):
        return BarSet(raw_data={'NOSYMBOL': []})

    monkeypatch.setattr(
        MODULE_PATH_GET_BARSET_ALPACA_API,
        _mock_get_barset_alpaca_api
    )