from alpaca.data.enums import Adjustment
from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame

from fixture.patch.api.alpaca.bar import patch_get_stock_bars_empty
from src.infra.api.alpaca.bar import AlpacaApiBarClient

cli = AlpacaApiBarClient()


def test_fx_replace_api_alpaca_get_stock_bars_empty(
    fx_replace_api_alpaca_get_stock_bars_empty
):
    """
    フィクスチャにより、get_stock_bars_empty()の置き換えが成功しているかを確認。
    テスト内容はほぼtest_patch_get_stock_bars_emptyと同じ。
    """
    barset_mock = cli.get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    assert 'NOSYMBOL_2602E09F' in barset_mock.data
    assert len(barset_mock.data['NOSYMBOL_2602E09F']) == 0
