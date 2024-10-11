from fixture.operate import load_table_bar_alpaca_on_db
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_cleanup_tables():
    # TODO: テーブルを空にできることを確認
    pass


def test_load_table_bar_alpaca_on_db():
    """
    テスト用関数load_table_bar_alpaca_on_db()の動作確認
    """
    load_table_bar_alpaca_on_db()
    result = TableBarAlpaca.select()
    # ファクトリのBar本数は10本
    assert len(result) == 10