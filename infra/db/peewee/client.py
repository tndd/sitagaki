from os import getenv
from typing import List

from peewee import Database, Model, MySQLDatabase, SqliteDatabase, chunked


def _create_db() -> Database:
    """
    動作モードに応じてDBを作成する
        * TEST: テスト用DB(MYSQL)
        * DEV: 開発用DB(MYSQL)
        * PROD: 本番用DB(MYSQL)
        * 指定なし: SQLite in memory
    """
    WORK_MODE = getenv('WORK_MODE', 'DEFAULT')
    if WORK_MODE == 'TEST':
        db = MySQLDatabase(
            'fuli_test',
            user='mysqluser',
            password='mysqlpassword',
            host='localhost',
            port=6002,
        )
    elif WORK_MODE == 'DEV':
        db = MySQLDatabase(
            'fuli_dev',
            user='mysqluser',
            password='mysqlpassword',
            host='localhost',
            port=6001,
        )
    elif WORK_MODE == 'PROD':
        db = MySQLDatabase(
            'fuli',
            user='mysqluser',
            password='mysqlpassword',
            host='localhost',
            port=6000,
        )
    else:
        # デフォルト動作はsqlite
        db = SqliteDatabase(':memory:')
    return db


_DB = _create_db()

# テーブル基底クラス
class PeeweeTable(Model):
    class Meta:
        database = _DB


# DB操作メソッド
def insert_models(
    models: List[Model],
    batch_size: int = 10000,
):
    """
    NOTE: インサート速度の向上方法調査
        sqlalchemyも試してみたが、そちらもおおよそ同じ早さ。
        並列化しようにもpeeweeの場合、ピクルか問題により難しい。
        ここは一旦棚上げした方が良さそう。
    """
    # モデルの型を取得
    TModel = type(models[0])
    # テーブルが存在しない場合にテーブルを作成
    if not TModel.table_exists():
        _DB.create_tables([TModel])
    # モデルをデータベースに挿入
    data = [model.__data__ for model in models]
    with _DB.atomic():
        for batch in chunked(data, batch_size):
            TModel.replace_many(batch).execute()

def exec_query(query):
    """
    WARN: queryを実行するメソッドの修正
        本来、peeweeのqueryは明示的にexecute()を呼び出す必要はない。
        だがクエリ実行はクライアントを介して行うという一貫性を持たせるため、
        このメソッドを用意する。

        それにクエリ実行の前後に何らかの処理を行うことも考えられるため、
        このメソッドは完全に合理的でないわけではないか？
    """
    return query

def cleanup_tables(keyword: str):
    """
    テーブルを空にする
    """
    if keyword != 'DELETE_ALL':
        raise ValueError("keywordが異なるため、truncate_tablesを実行できません。")

    with _DB.atomic():
        tables = _DB.get_tables()
        # テーブルを削除
        # LATER: テーブル依存関係によっては失敗するので修正
        for table in tables:
            _DB.execute_sql(f"DROP TABLE IF EXISTS {table}")
