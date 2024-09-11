from alpaca.data.models import Bar

from domain.materia.bar.model import Timeframe
from infra.db.table.bar import TblBarDayAlpaca
from infra.process.api.alpaca.historical import (
    convert_bar_alpaca_list_to_sqlm,
    extract_bar_alpaca_list_from_barset,
)
from tests.utils.factory.infra.api.alpaca import (
    generate_bar_alpaca_list,
    generate_barset_alpaca,
)


def test_extract_bar_alpaca_list_from_barset():
    """
    BarSetの中からBarのリストを取り出す機能のテスト
    """
    barset = generate_barset_alpaca()
    bars = extract_bar_alpaca_list_from_barset(barset)
    assert isinstance(bars, list)
    assert all(isinstance(bar, Bar) for bar in bars)


def test_convert_bar_alpaca_list_to_sqlm():
    bar_alpaca_list = generate_bar_alpaca_list()
    tbl_bars_alpaca = convert_bar_alpaca_list_to_sqlm(bar_alpaca_list, Timeframe.DAY)
    assert isinstance(tbl_bars_alpaca, list)
    assert all(isinstance(tbl_bar, TblBarDayAlpaca) for tbl_bar in tbl_bars_alpaca)