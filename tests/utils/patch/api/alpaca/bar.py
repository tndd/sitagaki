import pytest
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.models import BarSet

from tests.utils.factory.infra.api.alpaca.bar import generate_barset_alpaca


def patch_get_stock_bars(mocker):
    """
    通信をモックし、ダミーのBarSetを返す。
    """
    mocker.patch.object(
        StockHistoricalDataClient,
        'get_stock_bars',
        return_value=generate_barset_alpaca()
    )

def patch_get_stock_bars_empty(mocker):
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
