from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.factory.infra.db.peewee.table.bar import (
    generate_table_bar_alpaca,
    generate_table_bar_alpaca_list,
)

"""
MEMO:
    基本的にはTableBarAlpacaがテーブルクラスとして機能しているかを確認する。
    だがその他にも挿入や取得などの一通りの動作確認も行っておく。
"""


def test_table_bar_alpaca_is_created(test_peewee_cli):
    """
    bar_alpacaテーブルは作成されうるモデルであるかを確認。
    """
    # 投入用のTableBarAlpacaを作成
    table_bar_alpaca = generate_table_bar_alpaca()
    # テーブルに投入
    test_peewee_cli.insert_models([table_bar_alpaca])
    # テーブルの存在確認
    assert TableBarAlpaca.table_exists()


def test_table_bar_alpaca_list(test_peewee_cli):
    """
    TableBarAlpacaのリストを投入および取得の基本テスト。

    1. データが投入されたことを確認
    2. synbol=AAPL and timeframe=1 and adjustment = 1 のデータ取得
        ３件のデータが取得されることを確認
    3. adjustment=2のデータ取得
        ０件のデータが取得されることを確認
    """
    # 投入用のTableBarAlpacaを作成
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    # テーブルに投入
    test_peewee_cli.insert_models(table_bar_alpaca_list)
    # 1. データが投入されたことを確認
    assert len(TableBarAlpaca.select()) == len(table_bar_alpaca_list)
    # 2. symbol=AAPL and timeframe=1 and adjustment = 1 のデータ取得
    assert len(TableBarAlpaca.select().where(
        TableBarAlpaca.symbol == "AAPL",
        TableBarAlpaca.timeframe == 4,
        TableBarAlpaca.adjustment == 1,
    )) == 3
    # 3. adjustment=2のデータ取得
    assert len(TableBarAlpaca.select().where(
        TableBarAlpaca.adjustment == 2,
    )) == 0
