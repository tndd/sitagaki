from datetime import datetime

from src.domain.origin.alpaca.bar.model import SymbolTimestamp
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def arrive_symbol_timestamp_dict_from_table(
    tables: list[TableBarAlpaca],
    symbols: list[str] | None = None,
) -> dict[str, datetime | None]:
    """
    テーブルモデルリストをシンボルと日時の情報のみを抜き出し、
    symbolとtimeframeの辞書を返す。

    > テーブルリストに渡されたシンボルが存在しない場合
        timestamp=Noneとなる。

    > symbols未指定時の動作
        timestamp=Noneという変換は当然全く行われない。
        愚直な変換が行われる。

    NOTE: 存在しないsymbolのtimestampにNoneを入れる処理について
        本当はクエリの方でleft joinした結果を返しておけば話が早いんだが、
        クエリビルダーだけではそれが難しく、ややこしそうなのでこちらで処理する。
    """
    st_map = {table.symbol: table.timestamp for table in tables}
    # symbolsがNoneの場合、そのまま辞書を返す。
    if symbols is None:
        return st_map
    # symbols指定時、存在しないシンボルについてtimestamp=None処理を施す
    return {symbol: st_map.get(symbol, None) for symbol in symbols}
