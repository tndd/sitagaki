from src.domain.origin.alpaca.bar.model import SymbolTimestamp
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def arrive_symbol_timestamp_ls_from_table(
    tables: list[TableBarAlpaca],
    symbols: list[str] | None = None,
) -> list[SymbolTimestamp]:
    """
    テーブルモデルリストをシンボルと日時の情報のみを抜き出し、
    SymbolTimestampドメインモデルを生成する。

    > テーブルリストに渡されたシンボルが存在しない場合
        timestamp=NoneとしたSymbolTimestampに変換する。

    > 戻り値のlist[SymbolTimestamp]の順序
        symbolsの順番で帰る。

    > symbols未指定時の戻り値の順番
        tablesの順番

    > symbols未指定時の動作
        timestamp=Noneという変換は当然全く行われない

    NOTE: 存在しないsymbolのtimestampにNoneを入れる処理について
        本当はクエリの方でleft joinした結果を返しておけば話が早いんだが、
        クエリビルダーだけではそれが難しく、ややこしそうなのでこちらで処理する。
    """
    timestamp_map = {table.symbol: table.timestamp for table in tables}
    # symbolsがNoneの場合、とっととtablesをそのままlist[SymbolTimestamp]変換して返す
    if symbols is None:
        return [SymbolTimestamp(symbol=table.symbol, timestamp=table.timestamp) for table in tables]
    # symbols指定時、timestamp=Noneへの置き換え処理を行う
    symbol_timestamps = [
        SymbolTimestamp(
            symbol=symbol,
            timestamp=timestamp_map.get(symbol, None)  # 存在しない場合はNone
        )
        for symbol in symbols
    ]
    return symbol_timestamps
