from peewee import CharField, DatabaseProxy, Model, SqliteDatabase

from infra.db.peewee import PeeweeClient
from tests.utils.fixture.infra.db.peewee import db_proxy


class BaseModel(Model):
    class Meta:
        database = db_proxy

class User(BaseModel):
    username = CharField()
    email = CharField()


def test_insert_models(test_peewee_db):
    peewee_client = PeeweeClient(test_peewee_db)
    # 挿入するユーザーインスタンスのリストを作成
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
    ]
    # ユーザーデータ挿入
    peewee_client.insert_models(users)
    # 挿入されたユーザーを取得
    retrieved_users = User.select()
    # 取得したユーザーを検証
    assert len(retrieved_users) == 3
    assert retrieved_users[0].username == 'user1'
    assert retrieved_users[0].email == 'user1@example.com'
    assert retrieved_users[1].username == 'user2'
    assert retrieved_users[1].email == 'user2@example.com'
    assert retrieved_users[2].username == 'user3'
    assert retrieved_users[2].email == 'user3@example.com'


def test_insert_models_multiple(test_peewee_db):
    """
    複数回にわたって挿入する場合のテスト
    """
    peewee_client = PeeweeClient(test_peewee_db)
    # 挿入するユーザーインスタンスのリストを作成
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
    ]
    # 1回目の投入
    peewee_client.insert_models(users)
    retrieved_users = User.select()
    assert len(retrieved_users) == 3

    # 2回目の投入
    peewee_client.insert_models(users)
    retrieved_users = User.select()
    assert len(retrieved_users) == 6
