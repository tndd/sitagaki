from infra.db.peewee.client import PeeweeClient
from tests.utils.factory.infra.db.peewee.bar import generate_table_bar_alpaca_list


def prepare_test_bar_alpaca_on_db(db_cli: PeeweeClient) -> None:
    """
    テスト用のBarデータをDBに登録する。

    データはtimeframeで指定した先のテーブルに登録される。
    登録内容については、generate_table_bar_alpaca_list()の内容を参照。
    """
    bar_tables_alpaca = generate_table_bar_alpaca_list()
    db_cli.insert_models(bar_tables_alpaca)