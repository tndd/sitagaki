import pytest
from alpaca.data.models import BarSet

import infra.api.alpaca.bar
from tests.utils.generate.infra.api.alpaca.bar import generate_barset_alpaca


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
def patch_with_mock_get_barset_alpaca_api_fail_empty_barset(mocker):
    """
    空のBarSetを返す。
    ただし空のBarSetという戻り値はあり得ることなのでエラーではない。
    そのためerrではなくfailとしている。
    """
    mocker.patch.object(
        infra.api.alpaca.bar,
        'get_barset_alpaca_api',
        return_value=BarSet(raw_data={'NOSYMBOL': []})
    )
