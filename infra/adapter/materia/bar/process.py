from typing import List

from alpaca.data.models import Bar as BarAlpacaApi
from alpaca.data.models import BarSet as BarSetAlpacaApi

"""
TODO: やはりこれはapi/historicalに戻す。
    adapterをドメイン層に戻すのに伴い。
"""


def extract_bar_list_alpaca_api_from_barset(barset: BarSetAlpacaApi) -> List[BarAlpacaApi]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))
