from typing import List

from alpaca.data.models import Bar as BarAlpacaApi
from alpaca.data.models import BarSet as BarSetAlpacaApi

from domain.materia.bar.model import Bar, Timeframe
from infra.adapter.materia.bar import adapt_bar_domain_to_sqlm
from infra.db.table.bar import TableBarAlpaca


def extract_bar_list_alpaca_api_from_barset(barset: BarSetAlpacaApi) -> List[BarAlpacaApi]:
    """
    BarSetの中からBarのリストを取り出す。
    """
    return next(iter(barset.data.values()))


def convert_bar_list_alpaca_api_to_table(
        bars_alpaca_api: List[BarAlpacaApi],
        timeframe: Timeframe
) -> List[TableBarAlpaca]:
    """
    alpacaのバーのリストをDBのバーのリストに変換する。

    HACK: bar_alpaca_api -> bar_alpaca_tableへの変換過程
        本来であれば、
        "alpaca_api -> domain -> table"の順で変換が必要だが、
        "alpaca_api -> table"という直接変換を行う形式となってしまっている。

        たまたま、alpaca_apiのバーとdomainのバーは同じデータ構造をしているため、
        このような変換が可能になっている。
    """
    return [adapt_bar_domain_to_sqlm(bar, timeframe) for bar in bars_alpaca_api]