from alpaca.data.models import Bar

from domain.materia.bar.model import Timeframe
from infra.adapter.materia.bar.process import (
    convert_bar_list_alpaca_api_to_table,
    extract_bar_list_alpaca_api_from_barset,
)
from infra.db.table.bar import TableBarAlpaca
from tests.utils.factory.infra.api.alpaca import (
    generate_bar_alpaca_list,
    generate_barset_alpaca,
)


def test_extract_bar_alpaca_list_api_from_barset():
    """
    BarSetの中からBarのリストを取り出す機能のテスト
    """
    barset = generate_barset_alpaca()
    bars = extract_bar_list_alpaca_api_from_barset(barset)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)
