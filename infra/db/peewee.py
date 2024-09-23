from dataclasses import dataclass

from peewee import Database, DatabaseProxy, Model

db_proxy = DatabaseProxy()

@dataclass
class PeeweeClient:
    db: Database

    def __post_init__(self):
        self.db.connect()

    def insert_models(self, models: list[Model]):

        TModel = type(models[0])
        # テーブルが存在しない場合にテーブルを作成
        if not TModel.table_exists():
            self.db.create_tables([TModel])

        with self.db.atomic():
            TModel.bulk_create(models)


    def select_models(self, model: Model):
        pass
