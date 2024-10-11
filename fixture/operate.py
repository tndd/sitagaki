from typing import Sequence, cast

from fixture.decorator import test_only
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
