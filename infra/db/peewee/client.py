from typing import List

from peewee import Model, SqliteDatabase, chunked

# DB接続
DB = SqliteDatabase(':memory:')
DB.connect()

# テーブル基底クラス
class PeeweeTable(Model):
    class Meta:
        database = DB


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
        DB.create_tables([TModel])
    # モデルをデータベースに挿入
    data = [model.__data__ for model in models]
    with DB.atomic():
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

def truncate_tables(keyword: str):
    """
    テーブルを空にする
    """
    if keyword != 'TRUNCATE_TEST_TABLES':
        raise ValueError("keywordが異なるため、truncate_tablesを実行できません。")

    tables = DB.get_tables()
    with DB.atomic():
        for table in tables:
            DB.execute_sql(f"TRUNCATE TABLE {table}")
