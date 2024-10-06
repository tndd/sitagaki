import pytest
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.models import BarSet

from tests.utils.generate.infra.api.alpaca.bar import generate_barset_alpaca


@pytest.fixture
def fx_replace_with_mock_get_barset_alpaca_api_fail_empty_barset(mocker):
    patch_with_mock_get_barset_alpaca_api_fail_empty_barset(mocker)


def patch_with_mock_get_barset_alpaca_api(mocker):
    """
    通信をモックし、ダミーのBarSetを返す。
    """
    mocker.patch.object(
        StockHistoricalDataClient,
        'get_stock_bars',
        return_value=generate_barset_alpaca()
    )

def patch_with_mock_get_barset_alpaca_api_fail_empty_barset(mocker):
    """
    空のBarSetを返す。
    ただし空のBarSetという戻り値はあり得ることなのでエラーではない。
    そのためerrではなくfailとしている。
    """
    mocker.patch.object(
        StockHistoricalDataClient,
        'get_stock_bars',
        return_value=BarSet(raw_data={'NOSYMBOL': []})
    )
