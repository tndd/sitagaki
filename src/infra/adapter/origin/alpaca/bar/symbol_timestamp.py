from src.domain.origin.alpaca.bar.model import SymbolTimestamp
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def arrive_symbol_timestamp_ls_from_table(
    symbols: list[str],
    tables: list[TableBarAlpaca],
) -> list[SymbolTimestamp]:
    """
    テーブルモデルリストをシンボルと日時の情報のみを抜き出し、
    SymbolTimestampドメインモデルを生成する。

    テーブルリストに渡されたシンボルが存在しない場合は、
    timestamp=NoneとしたSymbolTimestampに変換する。

    NOTE: list[SymbolTimestamp]の順序
        symbolsの順番で帰る。

    NOTE: 存在しないsymbolのtimestampにNoneを入れる処理について
        本当はクエリの方でleft joinした結果を返しておけば話が早いんだが、
        クエリビルダーだけではそれが難しく、ややこしそうなのでこちらで処理する。
    """
    timestamp_map = {table.symbol: table.timestamp for table in tables}
    symbol_timestamps = [
        SymbolTimestamp(
            symbol=symbol,
            timestamp=timestamp_map.get(symbol, None)  # 存在しない場合はNone
        )
        for symbol in symbols
    ]
    return symbol_timestamps
