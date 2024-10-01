from typing import List

from peewee import Database, DatabaseProxy, Model

DB_PROXY = DatabaseProxy()


class PeeweeTable(Model):
    class Meta:
        database = DB_PROXY


class PeeweeClient:
    def __init__(self, db: Database):
        self.db = db
        self.db.connect()

    def insert_models(self, models: List[Model]):
        """
        FIXME: インサートパフォーマンスが悪すぎるので改善
            100万行のインサートで40sもかかっている。
            遅い要因はpeeweeかsqliteのどちらか。

            https://stackoverflow.com/questions/37500369/peewee-with-bulk-insert-is-very-slow-into-sqlite-db
            これによるとsqliteの制約によって速度低下が起こっている可能性がある。
            mysqlでは高速に動作しているとの報告もある。

            接続先をrdsに変更して詳細を確かめる。
        """
        # モデルの型を取得
        TModel = type(models[0])
        # テーブルが存在しない場合にテーブルを作成
        if not TModel.table_exists():
            self.db.create_tables([TModel])
        # モデルをデータベースに挿入
        data = [model.__data__ for model in models]
        with self.db.atomic():
            TModel.replace_many(data).execute()

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