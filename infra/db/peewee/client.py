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
        # モデルの型を取得
        TModel = type(models[0])
        # テーブルが存在しない場合にテーブルを作成
        if not TModel.table_exists():
            self.db.create_tables([TModel])
        # 10万件以上の同時挿入はクラッシュの危険あり
        BATCH_SIZE = 100000
        with self.db.atomic():
            for i in range(0, len(models), BATCH_SIZE):
                batch = models[i:i+BATCH_SIZE]
                data = [model.__data__ for model in batch]
                # モデルをデータベースに挿入
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