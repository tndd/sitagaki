from peewee import AutoField, CharField

from infra.db.peewee.client import PeeweeClient, PeeweeTable, create_peewee_client


# テスト用モデル
class __SampleUser(PeeweeTable):
    id = AutoField(primary_key=True)
    username = CharField()
    email = CharField()


def test_create_peewee_client():
    cli = create_peewee_client()
    assert isinstance(cli, PeeweeClient)


def test_insert_models(test_peewee_cli):
    """
    ３件のデータを投入し、その内容を確認する。
    """
    # 挿入するユーザーインスタンスのリストを作成
    users = [
        __SampleUser(username='user1', email='user1@example.com'),
        __SampleUser(username='user2', email='user2@example.com'),
        __SampleUser(username='user3', email='user3@example.com')
    ]
    # ユーザーデータ挿入
    test_peewee_cli.insert_models(users)
    # 挿入されたユーザーを取得
    retrieved_users = __SampleUser.select()
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
        __SampleUser(username='user1', email='user1@example.com'),
        __SampleUser(username='user2', email='user2@example.com'),
        __SampleUser(username='user3', email='user3@example.com')
    ]
    # 1回目の投入
    test_peewee_cli.insert_models(users)
    retrieved_users = __SampleUser.select()
    assert len(retrieved_users) == 3
    # 2回目の投入
    test_peewee_cli.insert_models(users)
    retrieved_users = __SampleUser.select()
    assert len(retrieved_users) == 6
    # さらにテーブル内容を確認する
    retrieved_users = __SampleUser.select().where(__SampleUser.username == 'user1')
    assert len(retrieved_users) == 2


def test_insert_models_performance(test_peewee_cli):
    """
    挿入性能のテスト

    bulk_createのスピード検証用。
    調査の結果、個別にmodel.save()を呼び出す場合の２倍のスピードが出た。
    """
    # データを作成
    N = 10000
    users = [
        __SampleUser(username=f'user{i}', email=f'user{i}@example.com') for i in range(N)
    ]
    # データ挿入
    test_peewee_cli.insert_models(users)
    # データ取得
    retrieved_users = __SampleUser.select()
    assert len(retrieved_users) == N


def test_practice_select_models(test_peewee_cli):
    """
    データ取得のテスト

    1. 単純な取得
        10件のデータが取得できていること
    2. aaa.comで絞り込み
        astar, barbaraの2件のデータのみ取得できていること
    3. aaa.comかつastarの絞り込み
        astarのデータのみ取得できていること
    4. aaa.com または bbb.comで絞り込み
        astar, barbara, casper, dominant, edward, froite
          6件のデータが取得できていること
    5. ddd.comで絞り込み
        何もデータが取得できないこと
    6. 正規表現: 名前がaから始まる
        astarのみ取得できていること
    7. 正規表現: 名前がjから始まる or 名前がrで終わる
        joseph, astar, casperの3件のデータが取得できていること
    """
    users = [
        __SampleUser(username='astar', email='user1@aaa.com'),
        __SampleUser(username='barbara', email='user2@aaa.com'),
        __SampleUser(username='casper', email='user3@bbb.com'),
        __SampleUser(username='dominant', email='user4@bbb.com'),
        __SampleUser(username='edward', email='user5@bbb.com'),
        __SampleUser(username='froite', email='user6@bbb.com'),
        __SampleUser(username='gabriel', email='user7@ccc.com'),
        __SampleUser(username='hannah', email='user8@ccc.com'),
        __SampleUser(username='isaac', email='user9@ccc.com'),
        __SampleUser(username='joseph', email='user10@ccc.com'),
    ]
    test_peewee_cli.insert_models(users)
    # 1. 単純な取得
    retrieved_users = __SampleUser.select()
    assert len(retrieved_users) == 10
    # 2. aaa.comで絞り込み
    retrieved_users = __SampleUser.select().where(__SampleUser.email.contains('aaa.com'))
    assert len(retrieved_users) == 2
    assert set(['astar', 'barbara']) == set(u.username for u in retrieved_users)
    # 3. aaa.comかつastarの絞り込み
    retrieved_users = __SampleUser.select().where(
        __SampleUser.email.contains('aaa.com')
        & (__SampleUser.username == 'astar')
    )
    assert len(retrieved_users) == 1
    # 4. aaa.com または bbb.comで絞り込み
    retrieved_users = __SampleUser.select().where(
        (
            __SampleUser.email.contains('aaa.com')
            | __SampleUser.email.contains('bbb.com')
        )
    )
    assert len(retrieved_users) == 6
    assert set(
        [
            'astar',
            'barbara',
            'casper',
            'dominant',
            'edward',
            'froite'
        ]
    ) == set(u.username for u in retrieved_users)
    # 5. ddd.comで絞り込み
    retrieved_users = __SampleUser.select().where(__SampleUser.email.contains('ddd.com'))
    assert len(retrieved_users) == 0
    # 6. 正規表現: 名前がaから始まる
    retrieved_users = __SampleUser.select().where(__SampleUser.username.startswith('a'))
    assert len(retrieved_users) == 1
    assert set(['astar']) == set(u.username for u in retrieved_users)
    # 7. 正規表現: 名前がjから始まる or 名前がrで終わる
    retrieved_users = __SampleUser.select().where((__SampleUser.username.startswith('j') | __SampleUser.username.endswith('r')))
    assert len(retrieved_users) == 3
    assert set(['joseph', 'astar', 'casper']) == set(u.username for u in retrieved_users)


def test_insert_duplicate_key(test_peewee_cli):
    """
    重複したキーを挿入した場合のテスト

    重複したキーを挿入した場合、上書きされること
    """
    # 1回目の挿入
    users = [
        __SampleUser(id=1, username='user1', email='user1@example.com'),
        __SampleUser(id=2, username='user2', email='user2@example.com'),
    ]
    test_peewee_cli.insert_models(users)
    assert len(__SampleUser.select()) == 2
    assert __SampleUser.select().where(__SampleUser.id == 1).get().username == 'user1'
    assert __SampleUser.select().where(__SampleUser.id == 2).get().username == 'user2'
    # 2回目の挿入
    users = [
        __SampleUser(id=1, username='user11', email='user11@example.com'),
        __SampleUser(id=2, username='user22', email='user22@example.com'),
    ]
    test_peewee_cli.insert_models(users)
    # 上書きされるが故に４件ではなく２件のみ
    assert len(__SampleUser.select()) == 2
    # 内容は上書きされていること
    assert __SampleUser.select().where(__SampleUser.id == 1).get().username == 'user11'
    assert __SampleUser.select().where(__SampleUser.id == 2).get().username == 'user22'
