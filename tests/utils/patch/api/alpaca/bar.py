import pytest
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.models import BarSet

from tests.utils.mock.infra.api.alpaca.bar import generate_barset_alpaca


@pytest.fixture
def fx_replace_patch_alpaca_get_stock_bars_empty(mocker):
    patch_alpaca_get_stock_bars_empty(mocker)


def patch_alpaca_get_stock_bars(mocker):
    """
    通信をモックし、ダミーのBarSetを返す。
    """
    mocker.patch.object(
        StockHistoricalDataClient,
        'get_stock_bars',
        return_value=generate_barset_alpaca()
    )

def patch_alpaca_get_stock_bars_empty(mocker):
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
