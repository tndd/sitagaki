import pytest
from alpaca.data.enums import Adjustment
from alpaca.data.models import BarSet
from alpaca.data.timeframe import TimeFrame

from fixture.patch.api.alpaca.bar import patch_get_stock_bars
from src.infra.api.alpaca.bar import AlpacaApiBarClient

cli = AlpacaApiBarClient()


def test_patch_get_stock_bars(mocker):
    # パッチ適用
    patch_get_stock_bars(mocker)
    barset_mock = cli.get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    # MOCKSYMBOL IDが一致してればモック化されてるのは確定
    assert 'MOCKSYMBOL_30C779F3' in barset_mock.data


def test_patch_get_stock_bars_empty():
    # TODO: テストを作成
    pass
