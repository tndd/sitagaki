from copy import deepcopy
from datetime import datetime

from sqlalchemy import and_
from sqlmodel import SQLModel, select

from infra.db.sqlmodel import SqlModelClient
from tests.factory.user import User, generate_sample_users


def assert_users_equal(db_users, original_users):
    # 件数確認
    assert len(db_users) == len(original_users)
    # 内容確認: nameでソートし１件ずつ突合
    db_users_sorted = sorted(db_users, key=lambda u: u.name)
    original_users_sorted = sorted(original_users, key=lambda u: u.name)
    for db_user, original_user in zip(db_users_sorted, original_users_sorted):
        assert db_user.id is not None
        assert db_user.created_at == original_user.created_at
        assert db_user.name == original_user.name
        assert db_user.email == original_user.email
        assert db_user.credit == original_user.credit


def test_insert_models(test_engine):
    cli = SqlModelClient(test_engine)
    # テーブルの作成
    SQLModel.metadata.create_all(test_engine)
    users = generate_sample_users()
    # cli.insert_models(users)実行時にusersの内容が解放されてしまうため
    users_copy_for_valid = deepcopy(users)
    ### テスト部分 ###
    cli.insert_models(users)
    # インサートされたかを確認
    with cli.session() as session:
        # データ取得
        db_users = session.exec(select(User)).all()
        assert_users_equal(db_users, users_copy_for_valid)


def test_select_models(test_engine):
    cli = SqlModelClient(test_engine)
    # テスト用データの登録
    SQLModel.metadata.create_all(test_engine)
    users = generate_sample_users()
    users_copy_for_valid = deepcopy(users)
    cli.insert_models(users)
    """
    テスト１:
    条件なしのselect
    内容がusersと一致するかの確認。

    select_modelsが機能していることと、
    conditionを渡さなくても問題ないことを確認
    """
    db_users = cli.select_models(User)
    assert_users_equal(db_users, users_copy_for_valid)
    """
    テスト２:
    日付範囲のテスト
        1: 2000年未満 -> nagisa,kazusa,aliceのデータが取得される
        2: 2000年以降 -> astar,helta,carol,david
        3: 2000年 ~ 2005年 -> astar,helta,carol
    """
    # 2-1
    db_users_before_2000 = cli.select_models(
        model=User,
        conditions={"created_at": User.created_at < datetime(2000, 1, 1)}
    )
    assert all(user.name in ["nagisa", "kazusa", "alice"] for user in db_users_before_2000)
    # 2-2
    db_users_after_2000 = cli.select_models(
        model=User,
        conditions={"created_at": User.created_at >= datetime(2000, 1, 1)}
    )
    assert all(user.name in ["astar", "helta", "carol", "david"] for user in db_users_after_2000)
    # 2-3
    db_users_2000_to_2005 = cli.select_models(
        model=User,
        conditions={
            "created_at": and_(
                User.created_at >= datetime(2000, 1, 1),
                User.created_at < datetime(2006, 1, 1)
            )
        }
    )
    assert all(user.name in ["astar", "helta", "carol"] for user in db_users_2000_to_2005)
    """
    テスト３:
    creditによる絞り込み
    - 100 ~ 500 -> helta,carol,david
    - 10000以上 -> nagisa,astar
    """
    """
    テスト4:
    メールアドレスによる絞り込み
    - @blmail -> nagisa,kazusa,alice
    - @stmail -> astar,helta
    - @blmail.tri -> nagisa,kazusa
    """
    """
    テスト5:
    複合条件による絞り込み
    - @blmailかつcredit10000以上 -> nagisa
    - @blmailかつ日付が1981以降 -> kazusa,alice
    """