from alpaca.data.models import Bar, BarSet

from infra.api.alpaca.bar import extract_bar_list_alpaca_api_from_barset
from tests.utils.generate.infra.api.alpaca.bar import generate_barset_alpaca


def test_extract_default():
    """
    BarSetの中からBarのリストを取り出す機能のテスト
    """
    # case1: 正常系
    barset_empty = generate_barset_alpaca()
    # BarSetの中からBarのリストを取り出す
    bars = extract_bar_list_alpaca_api_from_barset(barset_empty)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)


def test_extract_empty_barset():
    """
    空のBarSetからBarのリストを取り出す際のテスト

    例えばすでにDBのデータが最新で、
    updateを行った際の戻り値が空という事態を想定したテスト。

    期待結果:
        空のBarリストが返される。
    """
    # 空のBarSetを生成
    barset_empty = BarSet(raw_data={'NOSYMBOL': []})
    # BarSetの中からBarのリストを取り出す
    bars = extract_bar_list_alpaca_api_from_barset(barset_empty)
    assert isinstance(bars, list)
    assert len(bars) == 0