from copy import deepcopy

from sqlmodel import SQLModel, select

from infra.db.sqlmodel import SqlModelClient
from tests.factory.user import User, generate_sample_users


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
        # 件数確認
        assert len(db_users) == len(users)
        # 内容確認: idでソートし１件ずつ突合
        db_users_sorted = sorted(db_users, key=lambda u: u.name)
        users_sorted = sorted(users_copy_for_valid, key=lambda u: u.name)
        for db_user, original_user in zip(db_users_sorted, users_sorted):
            assert db_user.id is not None
            assert db_user.created_at == original_user.created_at
            assert db_user.name == original_user.name
            assert db_user.email == original_user.email
            assert db_user.credit == original_user.credit