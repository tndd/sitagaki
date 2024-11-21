from datetime import datetime

import pytest
from alpaca.data.enums import Adjustment
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.timeframe import TimeFrame

from common.logger import LOG
from fixture.infra.api.alpaca.bar import (
    factory_bar_alpaca,
    factory_bar_alpaca_list,
    factory_barset_alpaca,
    factory_barset_with_args,
    fx_replace_api_alpaca_get_stock_bars_empty,
    patch_get_stock_bars,
    patch_get_stock_bars_empty,
    patch_get_stock_bars_with_args,
)
from src.infra.api.alpaca.bar import CLI_ALPACA_BAR


### FIXTURE ###
def test_fx_replace_api_alpaca_get_stock_bars_empty(
    fx_replace_api_alpaca_get_stock_bars_empty
):
    """
    フィクスチャにより、get_stock_bars_empty()の置き換えが成功しているかを確認。
    テスト内容はほぼtest_patch_get_stock_bars_emptyと同じ。
    """
    barset_mock = CLI_ALPACA_BAR._get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    assert 'NOSYMBOL_2602E09F' in barset_mock.data
    assert len(barset_mock.data['NOSYMBOL_2602E09F']) == 0


### PATCH ###
def test_patch_get_stock_bars(mocker):
    # パッチ適用
    patch_get_stock_bars(mocker)
    barset_mock = CLI_ALPACA_BAR._get_barset_alpaca_api(
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
    barset_mock = CLI_ALPACA_BAR._get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    assert 'NOSYMBOL_2602E09F' in barset_mock.data
    assert len(barset_mock.data['NOSYMBOL_2602E09F']) == 0


def test_patch_get_stock_bars_with_args(mocker):
    patch_get_stock_bars_with_args(mocker)
    barset_mock = CLI_ALPACA_BAR._get_barset_alpaca_api(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW
    )
    assert isinstance(barset_mock, BarSet)
    symbol_str = next(iter(barset_mock.data))
    # 実行される時点でAlpacaSDK側のstartには、
    # \ Noneの場合2000-01-01 00:00:00が設定されるため、START=Noneではないのが正常。
    assert symbol_str == 'MOCK_AAPL|TF=1Day|AD=raw|START=2000-01-01 00:00:00|LIMIT=NONE'


### FACTORY ###
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


@pytest.mark.parametrize(
    'symbol, timeframe, adjustment',
    [
        ('AAPL', tf, adj)
        for tf in [TimeFrame.Day, TimeFrame.Hour, TimeFrame.Minute]
        for adj in Adjustment
    ]
)
def test_factory_barset_with_args(symbol, timeframe, adjustment):
    """
    timeframe,adjustmentとして渡された引数が正常に反映されているかを確認。
    start,limitについては未指定であるため文字列がNONEであることを確認する。
    """
    barset = factory_barset_with_args(
        symbol=symbol,
        timeframe=timeframe,
        adjustment=adjustment
    )
    assert isinstance(barset, BarSet)
    symbol_str = next(iter(barset.data))
    assert symbol_str == f'MOCK_{symbol}|TF={timeframe.value}|AD={adjustment.value}|START=NONE|LIMIT=NONE'
    # dataの中身については、とりあえず取得件数だけ確認しておく
    assert len(barset.data[symbol_str]) == 10


@pytest.mark.parametrize(
    'start, limit',
    [
        (datetime(2010, 1, 1, 12, 0, 0), 100),
        (datetime(2000, 1, 1), 10),
    ]
)
def test_factory_barset_with_args_start_limit(start, limit):
    """
    start,limit指定時の挙動を確認

    datetime(2000, 1, 1)という不完全な日付の入力であっても、
    2000-01-01 00:00:00として処理されエラーは起こらない。
    """
    barset = factory_barset_with_args(
        symbol='AAPL',
        timeframe=TimeFrame.Day,
        adjustment=Adjustment.RAW,
        start=start,
        limit=limit
    )
    symbol_str = next(iter(barset.data))
    assert symbol_str == f'MOCK_AAPL|TF=1Day|AD=raw|START={start}|LIMIT={limit}'
    LOG.info(f'symbol_str: {symbol_str}')
    # dataの中身については、とりあえず取得件数だけ確認しておく
    assert len(barset.data[symbol_str]) == 10
