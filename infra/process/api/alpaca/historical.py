from typing import List

from alpaca.data.models import BarSet

from domain.materia.bar.model import Bar, Timeframe
from infra.adapter.materia.bar import adapt_bar_domain_to_sqlm
from infra.db.table.bar import TblBarBase

# TODO: adapterをtable_bar_alpacaに対応させる


def extract_bar_alpaca_list_from_barset(barset: BarSet) -> List[Bar]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))


def convert_bar_alpaca_list_to_sqlm(
        bars_alpaca: List[Bar],
        timeframe: Timeframe
) -> List[TblBarBase]:
    """
    alpacaのバーのリストをDBのバーのリストに変換する。

    HACK: bar_alpaca -> bar_sqlmへの変換過程
        本来であれば、
        "alpaca -> domain -> sqlm"の順で変換が必要だが、
        "alpaca -> sqlm"という直接変換を行う形式となってしまっている。

        たまたま、alpacaのバーとdomainのバーは同じデータ構造をしているため、
        このような変換が可能になっている。
    """
    return [adapt_bar_domain_to_sqlm(bar, timeframe) for bar in bars_alpaca]