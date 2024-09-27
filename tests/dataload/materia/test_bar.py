from infra.db.peewee.table.bar import TableBarAlpaca
from tests.utils.dataload.materia.bar import prepare_test_bar_alpaca_on_db


def test_prepare_test_bar_alpaca_on_db(test_peewee_cli):
    """
    BarデータがDBに登録されることを確認する。
    """
    prepare_test_bar_alpaca_on_db(test_peewee_cli)
    result = TableBarAlpaca.select()
    # ファクトリのBar本数は6本
    assert len(result) == 6