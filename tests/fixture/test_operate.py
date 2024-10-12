import pytest
from peewee import OperationalError

from fixture.operate import cleanup_tables, load_table_bar_alpaca_on_db
from src.infra.db.peewee.table.alpaca.bar import TableBarAlpaca


def test_cleanup_tables():
    # テーブルにデータを登録し中身を確認
    load_table_bar_alpaca_on_db()
    result = TableBarAlpaca.select()
    assert len(result) == 10
    # テーブルを空にする
    cleanup_tables()
    result = TableBarAlpaca.select()
    # テーブルが消去されているので、件数の取得に失敗する
    with pytest.raises(OperationalError):
        assert len(result) == 0


def test_load_table_bar_alpaca_on_db():
    """
    テスト用関数load_table_bar_alpaca_on_db()の動作確認
    """
    load_table_bar_alpaca_on_db()
    result = TableBarAlpaca.select()
    # ファクトリのBar本数は10本
    assert len(result) == 10