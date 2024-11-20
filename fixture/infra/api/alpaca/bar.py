from datetime import datetime, timedelta

import pytest
from alpaca.data.enums import Adjustment
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.models.bars import Bar, BarSet
from alpaca.data.timeframe import TimeFrame

from src.infra.api.alpaca.bar import extract_bar_list_alpaca_api_from_barset


@pytest.fixture
def fx_replace_api_alpaca_get_stock_bars_empty(mocker):
    patch_get_stock_bars_empty(mocker)


def patch_get_stock_bars(mocker):
    """
    通信をモックし、ダミーのBarSetを返す。
    """
    mocker.patch.object(
        StockHistoricalDataClient,
        'get_stock_bars',
        return_value=factory_barset_alpaca()
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
        return_value=BarSet(raw_data={'NOSYMBOL_2602E09F': []})
    )

def patch_get_stock_bars_with_args(mocker):
    """
    通信をモックし、受け取った引数に応じたダミーBarSetを返す。

    モック対象はAlpacaSDKの関数であることに注意。
    """
    mock = mocker.patch.object(
        StockHistoricalDataClient,
        'get_stock_bars'
    )
    def side_effect(request_params):
        return factory_barset_with_args(
            symbol=request_params.symbol_or_symbols,
            timeframe=request_params.timeframe,
            adjustment=request_params.adjustment,
            start=request_params.start,
            limit=request_params.limit
        )

    mock.side_effect = side_effect

def factory_barset_alpaca() -> BarSet:
    """
    AAPLのデータを生成する。
    いずれも2023/4/1 10:00~14:00の1時間足データ。
    """
    raw_data_barset = {
        "MOCKSYMBOL_30C779F3": [
            {
                "t": datetime(2023, 4, 1, 10, 0),
                "o": 100.0,
                "h": 105.0,
                "l": 99.0,
                "c": 102.0,
                "v": 1000,
                "n": 50,
                "vw": 101.5
            },
            {
                "t": datetime(2023, 4, 1, 11, 0),
                "o": 102.0,
                "h": 106.0,
                "l": 101.0,
                "c": 105.0,
                "v": 1200,
                "n": 60,
                "vw": 103.5
            },
            {
                "t": datetime(2023, 4, 1, 12, 0),
                "o": 105.0,
                "h": 108.0,
                "l": 104.0,
                "c": 107.0,
                "v": 1500,
                "n": 70,
                "vw": 106.0
            },
            {
                "t": datetime(2023, 4, 1, 13, 0),
                "o": 107.0,
                "h": 110.0,
                "l": 106.0,
                "c": 109.0,
                "v": 1800,
                "n": 80,
                "vw": 108.0
            },
            {
                "t": datetime(2023, 4, 1, 14, 0),
                "o": 109.0,
                "h": 112.0,
                "l": 108.0,
                "c": 111.0,
                "v": 2000,
                "n": 90,
                "vw": 110.0
            }
        ]
    }
    return BarSet(raw_data_barset)


def factory_bar_alpaca() -> Bar:
    raw_data = {
        "t": datetime(2023, 4, 1, 10, 0),  # timestamp
        "o": 100.0,  # open
        "h": 105.0,  # high
        "l": 99.0,   # low
        "c": 102.0,  # close
        "v": 1000,   # volume
        "n": 50,     # trade_count
        "vw": 101.5  # vwap
    }
    return Bar(symbol="MOCKSYMBOL_076E9AE1", raw_data=raw_data)


def factory_bar_alpaca_list() -> list[Bar]:
    """
    BarSetはそのままだと使いづらいので、
    そこからBarのリストを抜き出して返す機能を関数化した。
    """
    return extract_bar_list_alpaca_api_from_barset(factory_barset_alpaca())


def factory_barset_with_args(
    symbol: str,
    timeframe: TimeFrame,
    adjustment: Adjustment,
    start: datetime | None = None,
    limit: int | None = None
):
    """
    渡された引数を元に、本物のAPIのような戻り値を返す。
    10件のBarSetを返すこととする。
    日付は1年ずつずれていく。

    基本的には引数が正常に渡されたことを確認する事が目的。

    > 仕様
        1. base_priceを基準として、年々緩やかに上昇（5ドルずつ）
        2. 各日の価格変動幅は基準価格の2%で設定
        3. OHLC（始値・高値・安値・終値）の関係性を保持
            * 高値 > 始値・終値 > 安値
            * 終値は高値と安値の間に設定
        4. 取引量（volume）と取引回数（trade_count）も徐々に増加
        5. VWAPは簡略化して始値と終値の平均に設定
        6. 小数点以下2桁に丸めて現実的な表示に

    > start
        これが未指定の場合、2000-01-01を開始日とする

    > limit
        これは本来apiの取得件数を制限するためのものである。
        ここではlimitの値は使われず10件を固定で返す仕様としている。
        limitの値はsymbolの文字列内で確認できる。
    """
    if start is None:
        start_date = datetime(2000, 1, 1, 12, 0, 0)
    else:
        start_date = start
    # モックデータの生成
    raw_data_mock = []
    for i in range(10):
        base_price = 100.0 + (i * 5)  # 基準価格は徐々に上昇
        volatility = base_price * 0.02  # 価格変動幅は基準価格の2%
        # OHLCの設定
        open_price = base_price
        high_price = base_price + volatility
        low_price = base_price - volatility
        close_price = base_price + (volatility * 0.3)  # 高値と安値の間で終わる

        raw_data_mock.append({
            "t": start_date + timedelta(days=365*i),
            "o": round(open_price, 2),
            "h": round(high_price, 2),
            "l": round(low_price, 2),
            "c": round(close_price, 2),
            "v": 10000 + (i * 1000),  # 取引量も徐々に増加
            "n": 500 + (i * 50),      # 取引回数も徐々に増加
            "vw": round((open_price + close_price) / 2, 2)  # VWAPは単純化して始値と終値の平均に
        })
    # 引数が未指定のものについてはNONEと表示させるようにする
    start_str = 'NONE' if start is None else start
    limit_str = 'NONE' if limit is None else limit
    # symbolから渡された引数を確認できるようにする
    symbol = f'MOCK_{symbol}|TF={timeframe.value}|AD={adjustment.value}|START={start_str}|LIMIT={limit_str}'
    return BarSet(raw_data={symbol: raw_data_mock})
