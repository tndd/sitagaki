from typing import List

from alpaca.data.timeframe import TimeFrame as TimeFrameAlpaca
from alpaca.data.timeframe import TimeFrameUnit

from domain.materia.bar.model import Bar, Timeframe
from infra.db.table.bar import TableBarAlpaca


def adapt_bar_sqlm(bar_sqlm: TblBarBase) -> Bar:
    return Bar.model_validate(bar_sqlm.model_dump())


def adapt_bar_list_sqlm(bars_sqlm: List[TblBarBase]) -> List[Bar]:
    """
    DBから取得したバーのリストをドメイン層のバーのリストに変換する。

    注意:
        このDB->domainの変換は、Timeframeを気にしない。
        なぜならdomain層のバーは、Timeframeを区別しないから。
    """
    return [adapt_bar_sqlm_to_domain(bar) for bar in bars_sqlm]
