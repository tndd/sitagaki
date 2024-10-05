import pytest
from alpaca.data.models import BarSet

import infra.api.alpaca.bar
from tests.utils.mock.infra.api.alpaca.bar import generate_barset_alpaca

MODULE_PATH_GET_BARSET_ALPACA_API = 'infra.api.alpaca.bar.get_barset_alpaca_api'


def patch_with_mock_get_barset_alpaca_api(mocker):
    """
    通信をモックし、ダミーのBarSetを返す。
    """
    mocker.patch.object(
        infra.api.alpaca.bar,
        'get_barset_alpaca_api',
        return_value=generate_barset_alpaca()
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