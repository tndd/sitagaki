from src.domain.origin.alpaca.bar.model import SymbolTimestamp, SymbolTimestampSet
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def arrive_symbol_timestamp_set_from_table(
    symbols: list[str],
    tables: list[TableBarAlpaca],
) -> SymbolTimestampSet:
    """
    テーブルモデルリストをシンボルと日時の情報のみを抜き出し、
    SymbolTimestampドメインモデルを生成する。

    テーブルリストに渡されたシンボルが存在しない場合は、
    timestamp=NoneとしたSymbolTimestampに変換する。

    NOTE: 存在しないsymbolのtimestampにNoneを入れる処理について
        本当はクエリの方でleft joinした結果を返しておけば話が早いんだが、
        クエリビルダーだけではそれが難しく、ややこしそうなのでこちらで処理する。
    """
    table_symbols = set(table.symbol for table in tables)
    no_exist_symbols = list(set(symbols) - table_symbols)
    # TODO: setの方針でいくのかも検討