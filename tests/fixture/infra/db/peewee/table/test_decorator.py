import pytest
from peewee import AutoField, CharField

from fixture.infra.db.peewee.table.decorator import auto_insert
from src.infra.db.peewee.client import PeeweeTable


def test_auto_insert():
    """
    auto_insertがテーブルへの挿入機能を果たせているかを確認。

    また引数INSERTを指定することで、
    挿入機能のON,OFFを切り替え可能であることも確認する。
    """
    TEST_TABLE_NAME = '__test_table_7cf5453d'
    # テスト用モデル
    class _SampleUser(PeeweeTable):
        id = AutoField(primary_key=True)
        username = CharField()
        email = CharField()
        class Meta:
            table_name = TEST_TABLE_NAME
    # テスト用モデル作成ファクトリ
    @auto_insert
    def _factory_sample_users(n: int):
        users = [
            _SampleUser(
                username=f'user{i}',
                email=f'user{i}@example.com'
            ) for i in range(n)
        ]
        return users
    ### テスト用モデル作成(auto_insert無効) ###
    N = 10 # モデル作成数
    users_off = _factory_sample_users(N) # デフォルト状態では無効となっている
    # テスト用モデルが作成されているかを確認
    assert len(users_off) == N
    assert all(isinstance(user, _SampleUser) for user in users_off)
    # データ挿入は行われていないので、データを取得することはできない
    with pytest.raises(Exception, match=f"no such table: {TEST_TABLE_NAME}"):
        users_from_db = _SampleUser.select()
        len(users_from_db) # ここでエラー発生が期待される

    ### テスト用モデル作成(auto_insert有効) ###
    users_on = _factory_sample_users(N, INSERT=True)
    # テスト用モデルが作成されているかを確認
    assert len(users_on) == N
    assert all(isinstance(user, _SampleUser) for user in users_on)
    # データ挿入が行われているので、データを取得することができる
    users_from_db = _SampleUser.select()
    assert len(users_from_db) == N