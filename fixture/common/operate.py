from typing import Sequence, cast

from fixture.common.decorator import only_test
from src.infra.db.peewee.client import CLI_PEEWEE


@only_test
def cleanup_tables():
    """
    テーブルを空にする。
    """
    with CLI_PEEWEE.db.atomic():
        table_names = cast(Sequence[str], CLI_PEEWEE.db.get_tables())
        # テーブルを削除
        for name in table_names:
            CLI_PEEWEE.db.execute_sql(f"DROP TABLE IF EXISTS {name}")
