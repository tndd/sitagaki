from fixture.infra.db.peewee.table.alpaca.bar import (
    generate_table_bar_alpaca,
    generate_table_bar_alpaca_list,
)
from src.infra.db.peewee.client import PeeweeClient
from src.infra.db.peewee.table.alpaca.bar import (
    AdjustmentTable,
    TableBarAlpaca,
    TimeframeTable,
)

peewee_cli = PeeweeClient()


def test_table_bar_alpaca_is_created():
    """
    bar_alpacaテーブルは作成されうるモデルであるかを確認。
    """
    # 投入用のTableBarAlpacaを作成
    table_bar_alpaca = generate_table_bar_alpaca()
    # テーブルに投入
    peewee_cli.insert_models([table_bar_alpaca])
    # テーブルの存在確認
    assert TableBarAlpaca.table_exists()


def test_table_bar_alpaca_list():
    """
    TableBarAlpacaのリストを投入および取得の基本テスト。

    1. データが投入されたことを確認
    2. synbol=AAPL and timeframe=DAY and adjustment=RAW のデータ取得
        ３件のデータが取得されることを確認
    3. adjustment=SPLITのデータ取得
        ０件のデータが取得されることを確認
    """
    # 投入用のTableBarAlpacaを作成
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    # テーブルに投入
    peewee_cli.insert_models(table_bar_alpaca_list)
    # 1. データが投入されたことを確認
    assert len(TableBarAlpaca.select()) == len(table_bar_alpaca_list)
    # 2. symbol=AAPL and timeframe=DAY and adjustment = RAW のデータ取得
    assert len(TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == "AAPL",
        TableBarAlpaca.timeframe == TimeframeTable.DAY,
        TableBarAlpaca.adjustment == AdjustmentTable.RAW,
    )) == 3
    # 3. adjustment=SPLITのデータが取得できないことを確認
    assert len(TableBarAlpaca.select().where(
        TableBarAlpaca.adjustment == AdjustmentTable.SPLIT,
    )) == 0
