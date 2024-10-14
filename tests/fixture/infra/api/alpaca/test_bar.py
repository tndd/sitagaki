from alpaca.data.enums import Adjustment
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.timeframe import TimeFrame

from fixture.infra.api.alpaca.bar import (
    factory_bar_alpaca,
    factory_bar_alpaca_list,
    factory_barset_alpaca,
    fx_replace_api_alpaca_get_stock_bars_empty,
    patch_get_stock_bars,
    patch_get_stock_bars_empty,
)
from src.infra.api.alpaca.bar import AlpacaApiBarClient

cli_alpaca_bar = AlpacaApiBarClient()


def test_fx_replace_api_alpaca_get_stock_bars_empty(
    fx_replace_api_alpaca_get_stock_bars_empty
):
    """
    フィクスチャにより、get_stock_bars_empty()の置き換えが成功しているかを確認。
    テスト内容はほぼtest_patch_get_stock_bars_emptyと同じ。
    """
    barset_mock = cli_alpaca_bar.get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    assert 'NOSYMBOL_2602E09F' in barset_mock.data
    assert len(barset_mock.data['NOSYMBOL_2602E09F']) == 0


def test_patch_get_stock_bars(mocker):
    # パッチ適用
    patch_get_stock_bars(mocker)
    barset_mock = cli_alpaca_bar.get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    # MOCKSYMBOL IDが一致してればモック化されてるのは確定
    assert 'MOCKSYMBOL_30C779F3' in barset_mock.data
    assert len(barset_mock.data['MOCKSYMBOL_30C779F3']) == 5


def test_patch_get_stock_bars_empty(mocker):
    patch_get_stock_bars_empty(mocker)
    barset_mock = cli_alpaca_bar.get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    assert 'NOSYMBOL_2602E09F' in barset_mock.data
    assert len(barset_mock.data['NOSYMBOL_2602E09F']) == 0


def test_factory_barset_alpaca():
    barset = factory_barset_alpaca()
    assert isinstance(barset, BarSet)
    assert 'MOCKSYMBOL_30C779F3' in barset.data

def test_factory_bar_alpaca():
    bar = factory_bar_alpaca()
    assert isinstance(bar, Bar)
    assert bar.symbol == 'MOCKSYMBOL_076E9AE1'


def test_factory_bar_alpaca_list():
    bars = factory_bar_alpaca_list()
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)