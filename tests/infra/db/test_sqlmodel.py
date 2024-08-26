from copy import deepcopy
from random import choices
from string import ascii_letters
from typing import List

from sqlmodel import Field, SQLModel, select

from infra.db.sqlmodel import SqlModelClient


# テスト用の追加モデル
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str


def create_test_user_models() -> List[User]:
    # ランダムにユーザーを10件作成
    users = []
    for _ in range(10):
        name = ''.join(choices(ascii_letters, k=8))
        email = f"{name.lower()}@example.com"
        users.append(User(name=name, email=email))
    return users


def test_insert_models(test_engine):
    cli = SqlModelClient(test_engine)
    # テーブルの作成
    SQLModel.metadata.create_all(test_engine)
    # ランダムにユーザーを10件作成
    users = create_test_user_models()
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
            assert db_user.name == original_user.name
            assert db_user.email == original_user.email