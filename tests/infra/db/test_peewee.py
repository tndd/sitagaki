from peewee import (
    BooleanField,
    CharField,
    Database,
    DateField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
)

from infra.db.peewee import PeeweeClient

db = SqliteDatabase(':memory:')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField()
    email = CharField()


def test_peewee():
    # 挿入するユーザーインスタンスのリストを作成
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
    ]
    # PeeweeClientを使用してデータベースにユーザーを挿入
    peewee_client = PeeweeClient(db)
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
