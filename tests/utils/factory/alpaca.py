from datetime import datetime
from typing import Dict, List, Optional

from alpaca.data.models import BarSet
from pydantic import BaseModel

from tests.utils.mock.loader import load


class MockBar(BaseModel):
    """
    alpacaのbarモデルは作成に手間がかかりすぎるので、
    代わりにモックデータでテストするようにする。
    """
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: Optional[float]
    vwap: Optional[float]


class MockBarSet(BaseModel):
    """
    alpacaのbarsetモデル作成はbarモデルよりはるかに面倒。
    要素さえ揃ってればテストできるだろうからこれで勘弁してくれ。

    参考: クラスの形状
        data:
            SYMBOL: [
                MOCKBAR1,
                MOCKBAR2,
                ...
            ]
    """
    data: Dict[str, List[MockBar]] = {}


def make_barset_mock_from_dict(data: dict) -> MockBarSet:
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
    # barモデルのリストの作成: AAPLのvaluesであるリスト部分を取得
    bar_dicts: List[dict] = next(iter(data['data'].values()))
    # bars
    bars: List[MockBar] = []
    for d in bar_dicts:
        d['timestamp'] = datetime.fromisoformat(d['timestamp'])
        bars.append(MockBar(**d))
    # barsetモデルの作成
    bars_symbol = next(iter(data['data'].keys()))
    barset_data = {bars_symbol: bars}
    # barsetモデルを返す
    return MockBarSet(
        data=barset_data
    )


def generate_barset_mock() -> MockBarSet:
    """
    mockにある特定のbarsetファイルに基づいたBarSetモデルを生成する
    """
    # barsetファイルの読み込み
    data = load('barset.json')
    # 生成したbarsetモデルを返す
    return make_barset_mock_from_dict(data)
