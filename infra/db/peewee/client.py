from dataclasses import dataclass
from typing import List

from peewee import Database, Model, MySQLDatabase, SqliteDatabase, chunked

from infra.db.common import WorkMode, get_work_mode


def create_db() -> Database:
    """
    動作モードに応じてDBを作成する
        * TEST: テスト用DB(MYSQL)
        * DEV: 開発用DB(MYSQL)
        * PROD: 本番用DB(MYSQL)
        * 指定なし: SQLite in memory
    """
    work_mode = get_work_mode()
    db_config = {
        WorkMode.TEST: {'name': 'fuli_test', 'port': 6002},
        WorkMode.DEV: {'name': 'fuli_dev', 'port': 6001},
        WorkMode.PROD: {'name': 'fuli', 'port': 6000},
    }
    if work_mode in db_config:
        return MySQLDatabase(
            **db_config[work_mode],
            user='mysqluser',
            password='mysqlpassword',
            host='localhost'
        )
    return SqliteDatabase(':memory:')

# peeweeの仕様上、ここでなんらかのDBをインスタンス化しておかねばならない
DB_PEEWEE = create_db()

# Peeweeテーブルの基底クラス
class PeeweeTable(Model):
    class Meta:
        database = DB_PEEWEE


@dataclass
class PeeweeClient:
    db: Database = DB_PEEWEE

    def is_test_mode(self) -> bool:
        """
        このクライアントがテストモードで動いているのかどうかを返す。
        """
        work_mode = get_work_mode()
        return work_mode is WorkMode.TEST \
            or work_mode is WorkMode.IN_MEMORY

    def insert_models(
        self,
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
            self.db.create_tables([TModel])
        # モデルをデータベースに挿入
        data = [model.__data__ for model in models]
        with self.db.atomic():
            for batch in chunked(data, batch_size):
                TModel.replace_many(batch).execute()

    def exec_query(self, query):
        """
        WARN: queryを実行するメソッドの修正
            本来、peeweeのqueryは明示的にexecute()を呼び出す必要はない。
            だがクエリ実行はクライアントを介して行うという一貫性を持たせるため、
            このメソッドを用意する。

            それにクエリ実行の前後に何らかの処理を行うことも考えられるため、
            このメソッドは完全に合理的でないわけではないか？
        """
        return query

    def exec_sqls(self, sqls: List[str]):
        """
        任意のSQLを実行する
        """
        with self.db.atomic():
            for sql in sqls:
                self.db.execute_sql(sql)
