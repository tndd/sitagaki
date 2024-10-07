from datetime import datetime

from alpaca.data.models.bars import Bar, BarSet

from infra.api.alpaca.bar import extract_bar_list_alpaca_api_from_barset


def generate_barset_alpaca() -> BarSet:
    """
    AAPLのデータを生成する。
    いずれも2023/4/1 10:00~14:00の1時間足データ。
    """
    raw_data_barset = {
        "MOCKSYMBOL": [
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


def generate_bar_alpaca() -> Bar:
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
    return Bar(symbol="AAPL", raw_data=raw_data)


def generate_bar_alpaca_list() -> list[Bar]:
    return extract_bar_list_alpaca_api_from_barset(generate_barset_alpaca())