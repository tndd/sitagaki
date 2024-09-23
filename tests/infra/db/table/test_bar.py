from infra.db.table.bar import TableBarAlpaca
from tests.utils.factory.infra.db.table.bar import generate_table_bar_alpaca


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
