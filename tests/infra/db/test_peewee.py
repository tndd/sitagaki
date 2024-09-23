from peewee import CharField

from infra.db.peewee import PeeweeClient, PeeweeTable


# テスト用モデル
class User(PeeweeTable):
    username = CharField()
    email = CharField()


def test_insert_models(test_peewee_cli):
    """
    ３件のデータを投入し、その内容を確認する。
    """
    # 挿入するユーザーインスタンスのリストを作成
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
    ]
    # ユーザーデータ挿入
    test_peewee_cli.insert_models(users)
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


def test_insert_models_multiple(test_peewee_cli):
    """
    複数回にわたって挿入する場合のテスト

    テスト内容
        1回目:
            * 3件のデータが挿入され、合計3件。
        2回目:
            * さらに3件のデータが挿入され、合計6件。
            * usernameが"user1"のデータが2件。
    """
    # 挿入するユーザーインスタンスのリストを作成
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
    ]
    # 1回目の投入
    test_peewee_cli.insert_models(users)
    retrieved_users = User.select()
    assert len(retrieved_users) == 3
    # 2回目の投入
    test_peewee_cli.insert_models(users)
    retrieved_users = User.select()
    assert len(retrieved_users) == 6
    # さらにテーブル内容を確認する
    retrieved_users = User.select().where(User.username == 'user1')
    assert len(retrieved_users) == 2
