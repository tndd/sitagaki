from datetime import datetime
from typing import List

from alpaca.data.mappings import BAR_MAPPING
from alpaca.data.models import Bar, BarSet

from tests.utils.mock.loader import load

# barデータをapiに模すために必要
REVERSED_BAR_MAPPING: dict = {v: k for k, v in BAR_MAPPING.items()}


def convert_bar_dict_to_api_format(data: dict) -> dict:
    """
    Barの辞書データをAlpaca APIの形式に変換する。
    """
    api_format = {}
    for key, value in data.items():
        if key in REVERSED_BAR_MAPPING:
            api_format[REVERSED_BAR_MAPPING[key]] = value
        else:
            api_format[key] = value
    return api_format


def make_barset_from_dict(data: dict) -> BarSet:
    """
    BarSetの辞書データからBarSetを作り出す。

    参考: 渡されるデータの例
        {
            "data": {
                "AAPL": [
                {
                    "symbol": "AAPL",
                    "timestamp": "2024-01-02 05:00:00+00:00",
                    "open": 187.15,
                    "high": 188.44,
                    "low": 183.885,
                    "close": 185.64,
                    "volume": 82496943.0,
                    "trade_count": 1009074.0,
                    "vwap": 185.937347
                },
                ...
                ]
            }
        }
    """
    # barモデルのリストの作成
    bar_dicts: List[dict] = next(iter(data['data'].values()))
    bars: List[Bar] = []
    for d in bar_dicts:
        """
        注意: alpaca Barの初期化(作成)方法について
            * alpacaのBarにはsymbol,timestamp,...という要素がある。
            * しかしBarを作成するにあたっては、これらの要素を直接渡して作ることはできない。
            * alpacaBarのコンストラクタによれば、
                    "def __init__(self, symbol: str, raw_data: RawData)"
                というふうに、symbolと残りの辞書データをRawDataとして渡す形式となっている。

        注意: Barの初期化時に渡すRawDataの形式
            * RawDataのキーの形は、open,highのような形式ではない。
            * apiのレスポンスに準拠した形であるo,hとなっていなければならない。
            * BARMAPPINGを参考に。
        """
        # mockデータをapi形式に変換
        d_api = convert_bar_dict_to_api_format(d)
        # タイムスタンプを文字列からdatetime型に変換
        d_api['t'] = datetime.fromisoformat(d_api['t'])
        # RawDataはsymbolを除いたデータであるため、ここで分離
        symbol = d_api.pop('symbol')
        # Barオブジェクトを作成してリストに追加
        bars.append(Bar(symbol=symbol, raw_data=d_api))
    # barsetモデルの作成
    bars_symbol = next(iter(data['data'].keys()))
    barset_data = {bars_symbol: bars}
    # barsetモデルを返す
    return BarSet(
        raw_data=barset_data
    )


def generate_barset() -> BarSet:
    """
    mockにある特定のbarsetファイルに基づいたBarSetモデルを生成する
    """
    # barsetファイルの読み込み
    data = load('barset.json')
    # 生成したbarsetモデルを返す
    return make_barset_from_dict(data)
