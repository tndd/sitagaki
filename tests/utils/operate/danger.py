from typing import Sequence, cast

from infra.db.common import is_test_mode
from infra.db.peewee.client import PeeweeClient

peewee_cli = PeeweeClient()


def cleanup_tables():
    """
    テーブルを空にする。
    """
    if not is_test_mode():
        raise ValueError("テストモードではないため、cleanup_tablesを実行できません。")
    with peewee_cli.db.atomic():
        table_names = cast(Sequence[str], peewee_cli.db.get_tables())
        # テーブルを削除
        for name in table_names:
            peewee_cli.db.execute_sql(f"DROP TABLE IF EXISTS {name}")
