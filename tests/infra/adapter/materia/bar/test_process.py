from alpaca.data.models import Bar

from infra.adapter.materia.bar.process import extract_bar_list_alpaca_api_from_barset
from tests.utils.factory.infra.api.alpaca import generate_barset_alpaca


def test_extract_bar_alpaca_list_api_from_barset():
    """
    BarSetの中からBarのリストを取り出す機能のテスト
    """
    barset = generate_barset_alpaca()
    bars = extract_bar_list_alpaca_api_from_barset(barset)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)
