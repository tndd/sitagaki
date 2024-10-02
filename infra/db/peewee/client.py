from typing import List

from peewee import Database, DatabaseProxy, Model, chunked

DB_PROXY = DatabaseProxy()


class PeeweeTable(Model):
    class Meta:
        database = DB_PROXY


class PeeweeClient:
    def __init__(self, db: Database):
        self.db = db
        self.db.connect()

    def insert_models(
            self,
            models: List[Model],
            batch_size: int = 10000,
    ):
        """
        TODO: インサートパフォーマンスが悪すぎるので改善
            むしろsqliteの方が高速に動作している。
            だが本番では大量のデータを取り扱う以上、mysqlに変更する必要がある。
            なら高速化するなら並列化あたりだろうか？
            あるいは保存すべきデータをキャッシュで保存し、逐次インサートするという方法か。
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