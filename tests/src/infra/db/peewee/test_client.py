from peewee import AutoField, CharField

from src.infra.db.peewee.client import CLI_PEEWEE, PeeweeTable

TEST_TABLE_NAME = '__test_user_f3875f7f'


# テスト用モデル
class SampleUser(PeeweeTable):
    id = AutoField(primary_key=True)
    username = CharField()
    email = CharField()

    class Meta:
        # テーブル名を重複させないため
        table_name = TEST_TABLE_NAME


def factory_test_users(n: int) -> list[SampleUser]:
    """
    N件のサンプルユーザーを生成する。
    """
    return [
        SampleUser(
            username=f'user{i}',
            email=f'user{i}@example.com'
        ) for i in range(1, n+1)
    ]

def insert_test_users(n: int):
    """
    N件のサンプルユーザーを挿入する。
    """
    users = factory_test_users(n)
    CLI_PEEWEE.insert_models(users)


### TEST ###
def test_insert_models():
    """
    ３件のデータを投入し、その内容を確認する。
    """
    N = 3
    # サンプルユーザーを挿入
    insert_test_users(N)
    # 挿入されたユーザーを取得
    retrieved_users = SampleUser.select()
    # 取得したユーザーを検証
    assert len(retrieved_users) == N
    assert retrieved_users[0].username == 'user1'
    assert retrieved_users[0].email == 'user1@example.com'
    assert retrieved_users[1].username == 'user2'
    assert retrieved_users[1].email == 'user2@example.com'
    assert retrieved_users[2].username == 'user3'
    assert retrieved_users[2].email == 'user3@example.com'


def test_insert_models_multiple():
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
    users = factory_test_users(3)
    # 1回目の投入
    CLI_PEEWEE.insert_models(users)
    retrieved_users = SampleUser.select()
    assert len(retrieved_users) == 3
    # 2回目の投入
    CLI_PEEWEE.insert_models(users)
    retrieved_users = SampleUser.select()
    assert len(retrieved_users) == 6
    # さらにテーブル内容を確認する
    retrieved_users = SampleUser.select().where(SampleUser.username == 'user1')
    assert len(retrieved_users) == 2


def test_insert_models_performance():
    """
    挿入性能のテスト

    bulk_createのスピード検証用。
    調査の結果、個別にmodel.save()を呼び出す場合の２倍のスピードが出た。
    """
    N = 10000
    insert_test_users(N)
    # データ取得
    retrieved_users = SampleUser.select()
    assert len(retrieved_users) == N


def test_practice_select_models():
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
        SampleUser(username='astar', email='user1@aaa.com'),
        SampleUser(username='barbara', email='user2@aaa.com'),
        SampleUser(username='casper', email='user3@bbb.com'),
        SampleUser(username='dominant', email='user4@bbb.com'),
        SampleUser(username='edward', email='user5@bbb.com'),
        SampleUser(username='froite', email='user6@bbb.com'),
        SampleUser(username='gabriel', email='user7@ccc.com'),
        SampleUser(username='hannah', email='user8@ccc.com'),
        SampleUser(username='isaac', email='user9@ccc.com'),
        SampleUser(username='joseph', email='user10@ccc.com'),
    ]
    CLI_PEEWEE.insert_models(users)
    # 1. 単純な取得
    retrieved_users = SampleUser.select()
    assert len(retrieved_users) == 10
    # 2. aaa.comで絞り込み
    retrieved_users = SampleUser.select().where(SampleUser.email.contains('aaa.com'))
    assert len(retrieved_users) == 2
    assert set(['astar', 'barbara']) == set(u.username for u in retrieved_users)
    # 3. aaa.comかつastarの絞り込み
    retrieved_users = SampleUser.select().where(
        SampleUser.email.contains('aaa.com')
        & (SampleUser.username == 'astar')
    )
    assert len(retrieved_users) == 1
    # 4. aaa.com または bbb.comで絞り込み
    retrieved_users = SampleUser.select().where(
        (
            SampleUser.email.contains('aaa.com')
            | SampleUser.email.contains('bbb.com')
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
    retrieved_users = SampleUser.select().where(SampleUser.email.contains('ddd.com'))
    assert len(retrieved_users) == 0
    # 6. 正規表現: 名前がaから始まる
    retrieved_users = SampleUser.select().where(SampleUser.username.startswith('a'))
    assert len(retrieved_users) == 1
    assert set(['astar']) == set(u.username for u in retrieved_users)
    # 7. 正規表現: 名前がjから始まる or 名前がrで終わる
    retrieved_users = SampleUser.select().where((SampleUser.username.startswith('j') | SampleUser.username.endswith('r')))
    assert len(retrieved_users) == 3
    assert set(['joseph', 'astar', 'casper']) == set(u.username for u in retrieved_users)


def test_insert_duplicate_key():
    """
    重複したキーを挿入した場合のテスト

    重複したキーを挿入した場合、上書きされること
    """
    # 1回目の挿入
    users = [
        SampleUser(id=1, username='user1', email='user1@example.com'),
        SampleUser(id=2, username='user2', email='user2@example.com'),
    ]
    CLI_PEEWEE.insert_models(users)
    assert len(SampleUser.select()) == 2
    assert SampleUser.select().where(SampleUser.id == 1).get().username == 'user1'
    assert SampleUser.select().where(SampleUser.id == 2).get().username == 'user2'
    # 2回目の挿入
    users = [
        SampleUser(id=1, username='user11', email='user11@example.com'),
        SampleUser(id=2, username='user22', email='user22@example.com'),
    ]
    CLI_PEEWEE.insert_models(users)
    # 上書きされるが故に４件ではなく２件のみ
    assert len(SampleUser.select()) == 2
    # 内容は上書きされていること
    assert SampleUser.select().where(SampleUser.id == 1).get().username == 'user11'
    assert SampleUser.select().where(SampleUser.id == 2).get().username == 'user22'


def test_exec_sql_fetch():
    """
    exec_sql_fetchのテスト
    """
    # テーブルにデータを挿入
    insert_test_users(10)
    sql = f"SELECT * FROM {TEST_TABLE_NAME} WHERE id % 2 = 0"
    retrieved_users = CLI_PEEWEE.exec_sql_fetch(sql)
    # データが取得できていること
    assert len(retrieved_users) == 5
    assert all(user['id'] % 2 == 0 for user in retrieved_users)