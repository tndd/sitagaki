import pytest
from peewee import OperationalError

from fixture.common.operate import cleanup_tables
from fixture.infra.db.peewee.table.alpaca.bar import (
    TableBarAlpaca,
    load_table_bar_alpaca_on_db,
)


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
