from dataclasses import dataclass
from typing import List

from peewee import (
    Database,
    DatabaseProxy,
    Model,
    MySQLDatabase,
    SqliteDatabase,
    chunked,
)

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
DB_PROXY = DatabaseProxy()

# Peeweeテーブルの基底クラス
class PeeweeTable(Model):
    class Meta:
        database = DB_PROXY


@dataclass
class PeeweeClient:
    db: Database = create_db()
    work_mode: WorkMode = get_work_mode()

    def __post_init__(self):
        """
        このクライアントをインスタンス化することで、
        初めてデータベースが実体化する。

        全てのDB操作はここで行われるのだから、
        initializeはモジュール内ではなくここで行うのが妥当。
        """
        DB_PROXY.initialize(self.db)

    def is_test_mode(self) -> bool:
        """
        このクライアントがテストモードで動いているのかどうかを返す。
        """
        return self.work_mode is WorkMode.TEST \
            or self.work_mode is WorkMode.IN_MEMORY

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

    def exec_sqls(self, sqls: List[str]):
        """
        任意のSQLを実行する
        """
        with self.db.atomic():
            for sql in sqls:
                self.db.execute_sql(sql)

    def cleanup_tables(self, keyword: str):
        """
        >>>DANGER<<<

        テーブルを空にする。
        """
        work_mode = get_work_mode()
        if work_mode not in (WorkMode.IN_MEMORY, WorkMode.TEST):
            raise ValueError(f"cleanup_tablesはテストモードのみ実行可能。現在のモード: {work_mode}")
        if keyword != 'DELETE_ALL':
            # あまりに危険なので２重にチェック
            raise ValueError("keywordが異なるため、truncate_tablesを実行できません。")
        with self.db.atomic():
            tables = self.db.get_tables()
            # テーブルを削除
            # LATER: テーブル依存関係によっては失敗するので修正
            for table in tables:
                self.db.execute_sql(f"DROP TABLE IF EXISTS {table}")
