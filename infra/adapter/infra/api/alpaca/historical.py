from typing import List

from alpaca.data.models import BarSet

from domain.materia.bar.model import Bar


def extract_bar_alpaca_list_from_barset(barset: BarSet) -> List[Bar]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))