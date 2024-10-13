from typing import Sequence, cast

from fixture.common.decorator import only_test
from src.infra.db.peewee.client import PEEWEE_CLI as peewee_cli


@only_test
def cleanup_tables():
    """
    テーブルを空にする。
    """
    with peewee_cli.db.atomic():
        table_names = cast(Sequence[str], peewee_cli.db.get_tables())
        # テーブルを削除
        for name in table_names:
            peewee_cli.db.execute_sql(f"DROP TABLE IF EXISTS {name}")
