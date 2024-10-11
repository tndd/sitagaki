from typing import Sequence, cast

from fixture.decorator import test_only
from fixture.factory.infra.db.peewee.bar import generate_table_bar_alpaca_list
from src.infra.db.peewee.client import PeeweeClient

peewee_cli = PeeweeClient()


@test_only
def cleanup_tables():
    """
    テーブルを空にする。
    """
    with peewee_cli.db.atomic():
        table_names = cast(Sequence[str], peewee_cli.db.get_tables())
        # テーブルを削除
        for name in table_names:
            peewee_cli.db.execute_sql(f"DROP TABLE IF EXISTS {name}")


def load_table_bar_alpaca_on_db():
    """
    BarデータをDBに登録する。
    """
    table_bar_alpaca_list = generate_table_bar_alpaca_list()
    peewee_cli.insert_models(table_bar_alpaca_list)
