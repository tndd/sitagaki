import infra.db.peewee.client as peewee_cli


def cleanup_for_test():
    """
    テスト用にテーブルをまっさらにする。
    """
    cleanup_on_db()


def cleanup_on_db():
    """
    DBのデータを削除する。
    """
    peewee_cli.cleanup_tables('DELETE_ALL')
