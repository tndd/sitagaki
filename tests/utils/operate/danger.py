from infra.db.peewee.client import PeeweeClient

peewee_cli = PeeweeClient()


def cleanup_tables():
    """
    テーブルを空にする。
    """
    if not peewee_cli.is_test_mode():
        raise ValueError("テストモードではないため、cleanup_tablesを実行できません。")
    with peewee_cli.db.atomic():
        tables = peewee_cli.db.get_tables()
        # テーブルを削除
        for table in tables:
            peewee_cli.db.execute_sql(f"DROP TABLE IF EXISTS {table}")
