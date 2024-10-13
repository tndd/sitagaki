from typing import Sequence, cast

from fixture.common.decorator import only_test
from src.infra.db.peewee.client import PEEWEE_CLI


@only_test
def cleanup_tables():
    """
    テーブルを空にする。
    """
    with PEEWEE_CLI.db.atomic():
        table_names = cast(Sequence[str], PEEWEE_CLI.db.get_tables())
        # テーブルを削除
        for name in table_names:
            PEEWEE_CLI.db.execute_sql(f"DROP TABLE IF EXISTS {name}")
