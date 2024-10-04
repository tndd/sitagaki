from infra.db.peewee.table.bar import TableBarAlpaca


def test_prepare_table_bar_alpaca_on_db(
    prepare_table_bar_alpaca_on_db,
):
    """
    BarデータがDBに登録されることを確認する。
    """
    result = TableBarAlpaca.select()
    # ファクトリのBar本数は10本
    assert len(result) == 10