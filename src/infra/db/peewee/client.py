from dataclasses import dataclass
from typing import Sequence

from peewee import (
    Database,
    DatabaseProxy,
    Model,
    ModelSelect,
    MySQLDatabase,
    SqliteDatabase,
    chunked,
)

from src.infra.db.common import CURRENT_WORK_MODE, WorkMode

_DB_PROXY: DatabaseProxy = DatabaseProxy()


def create_db() -> Database:
    """
    動作モードに応じてDBを作成する
        * TEST: テスト用DB(MYSQL)
        * DEV: 開発用DB(MYSQL)
        * PROD: 本番用DB(MYSQL)
        * 指定なし: SQLite in memory
    """
    db_config = {
        WorkMode.TEST: {'name': 'fuli_test', 'port': 6002},
        WorkMode.DEV: {'name': 'fuli_dev', 'port': 6001},
        WorkMode.PROD: {'name': 'fuli', 'port': 6000},
    }
    if CURRENT_WORK_MODE in db_config:
        return MySQLDatabase(
            **db_config[CURRENT_WORK_MODE],
            user='mysqluser',
            password='mysqlpassword',
            host='localhost'
        )
    elif CURRENT_WORK_MODE is WorkMode.IN_MEMORY:
        return SqliteDatabase(':memory:')
    raise ValueError(f"指定されたワークモードは存在しません: {CURRENT_WORK_MODE}")


# Peeweeテーブルの基底クラス
class PeeweeTable(Model):
    class Meta:
        database = _DB_PROXY


@dataclass
class PeeweeClient:
    db: Database = _DB_PROXY

    def insert_models(
        self,
        models: Sequence[Model],
        batch_size: int = 10000,
    ):
        """
        MEMO: インサート速度の向上方法調査
            sqlalchemyも試してみたが、そちらもおおよそ同じ早さ。
            並列化しようにもpeeweeの場合、ピクルか問題により難しい。
            ここは一旦棚上げした方が良さそう。
        """
        # モデルの型を取得
        model_t = type(models[0])
        # テーブルが存在しない場合にテーブルを作成
        if not model_t.table_exists():
            self.db.create_tables([model_t])
        # モデルをデータベースに挿入
        data = [model.__data__ for model in models]
        with self.db.atomic():
            for batch in chunked(data, batch_size):
                model_t.replace_many(batch).execute()

    def exec_query_fetch(self, query: ModelSelect) -> Sequence[Model]:
        """
        WARN: queryを実行するメソッドの修正
            本来、peeweeのqueryは明示的にexecute()を呼び出す必要はない。
            だがクエリ実行はクライアントを介して行うという一貫性を持たせるため、
            このメソッドを用意する。

            それにクエリ実行の前後に何らかの処理を行うことも考えられるため、
            このメソッドは完全に合理的でないわけではないか？
        """
        return list(query)

    def exec_sql_fetch(self, sql: str) -> Sequence[dict]:
        """
        任意の生SQLを実行する
        実行結果はカラム名と値の辞書形式のリストとして返される
        """
        with self.db.atomic():
            cursor = self.db.execute_sql(sql)
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]



# データベースを初期化
db = create_db()
_DB_PROXY.initialize(db)
# シングルトンなpeewee_cli
CLI_PEEWEE = PeeweeClient(db)
