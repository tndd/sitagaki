from copy import deepcopy
from datetime import datetime

from sqlmodel import between, select

from tests.utils.factory.tests.sample_user import (SampleUser,
                                                   generate_sample_users)


def assert_sample_users_equal(db_users, original_users):
    """
    SampleUserクラスが等しいかを確認する。
    """
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


def test_insert_models(test_sqlm_cli):
    users = generate_sample_users()
    # cli.insert_models(users)実行時にusersの内容が解放されてしまうため
    users_copy_for_valid = deepcopy(users)
    ### テスト部分 ###
    test_sqlm_cli.insert_models(users)
    # インサートされたかを確認
    with test_sqlm_cli.session() as session:
        # データ取得
        db_users = session.exec(select(SampleUser)).all()
        assert_sample_users_equal(db_users, users_copy_for_valid)


def test_select_models(test_sqlm_cli):
    users = generate_sample_users()
    users_copy_for_valid = deepcopy(users)
    test_sqlm_cli.insert_models(users)
    """
    テスト１:
    条件なしのselect
    内容がusersと一致するかの確認。

    select_modelsが機能していることと、
    conditionを渡さなくても問題ないことを確認
    """
    def select_stmt_all_sample_user():
        return select(SampleUser)

    stmt = select_stmt_all_sample_user()
    db_users = test_sqlm_cli.select_models(stmt)
    assert_sample_users_equal(db_users, users_copy_for_valid)
    """
    テスト２:
    日付範囲のテスト
        1: 2000年未満 -> nagisa,kazusa,aliceのデータが取得される
        2: 2000年以降 -> astar,helta,carol,david
        3: 2000年 ~ 2005年 -> astar,helta,carol
    """
    # 2-1: 2000年未満
    stmt = select(SampleUser).where(SampleUser.created_at < datetime(2000, 1, 1))
    db_users_before_2000 = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["nagisa", "kazusa", "alice"] for user in db_users_before_2000)

    # 2-2: 2000年以降
    stmt = select(SampleUser).where(SampleUser.created_at >= datetime(2000, 1, 1))
    db_users_after_2000 = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["astar", "helta", "carol", "david"] for user in db_users_after_2000)

    # 2-3: 2000年 ~ 2005年
    stmt = select(SampleUser).where(between(SampleUser.created_at, datetime(2000, 1, 1), datetime(2005, 12, 31)))
    db_users_2000_to_2005 = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["astar", "helta", "carol"] for user in db_users_2000_to_2005)

    """
    テスト３:
    creditによる絞り込み
        1: 100 ~ 500 -> helta,carol,david
        2: 10000以上 -> nagisa,astar
    """
     # 3-1: 100 ~ 500
    stmt = select(SampleUser).where(between(SampleUser.credit, 100, 500))
    db_users_credit_100_to_500 = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["helta", "carol", "david"] for user in db_users_credit_100_to_500)

    # 3-2: 10000以上
    stmt = select(SampleUser).where(SampleUser.credit >= 10000)
    db_users_credit_10000_or_above = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["nagisa", "astar"] for user in db_users_credit_10000_or_above)

    """
    テスト4:
    メールアドレスによる絞り込み
        1: @blmail -> nagisa,kazusa,alice
        2: @stmail -> astar,helta
        3: @blmail.tri -> nagisa,kazusa
    """
    # 4-1: @blmail
    stmt = select(SampleUser).where(SampleUser.email.like("%@blmail%"))
    db_users_blmail = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["nagisa", "kazusa", "alice"] for user in db_users_blmail)

    # 4-2: @stmail
    stmt = select(SampleUser).where(SampleUser.email.like("%@stmail%"))
    db_users_stmail = test_sqlm_cli.select_models(stmt)
    db_users_stmail = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["astar", "helta"] for user in db_users_stmail)

    # 4-3: @blmail.tri
    stmt = select(SampleUser).where(SampleUser.email.like("%@blmail.tri%"))
    db_users_blmail_tri = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["nagisa", "kazusa"] for user in db_users_blmail_tri)

    """
    テスト5:
    複合条件による絞り込み
        1: @blmailかつcredit10000以上 -> nagisa
        2: @blmailかつ日付が1981以降 -> kazusa,alice
    """
    # 5-1: @blmailかつcredit10000以上
    stmt = select(SampleUser).where(SampleUser.email.like("%@blmail%"), SampleUser.credit >= 10000)
    db_users_blmail_credit_10000_or_above = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["nagisa"] for user in db_users_blmail_credit_10000_or_above)

    # 5-2: @blmailかつ日付が1981以降
    stmt = select(SampleUser).where(SampleUser.email.like("%@blmail%"), SampleUser.created_at >= datetime(1981, 1, 1))
    db_users_blmail_after_1981 = test_sqlm_cli.select_models(stmt)
    assert all(user.name in ["kazusa", "alice"] for user in db_users_blmail_after_1981)