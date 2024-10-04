import infra.db.peewee.client as peewee_cli


def cleanup_for_test():
    """
    テスト用にテーブルをまっさらにする。
    """
    # DBの初期化
    peewee_cli.cleanup_tables('DELETE_ALL')
