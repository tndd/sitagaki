import pytest
from peewee import AutoField, CharField

import src.infra.db.common as common
from fixture.common.decorator import auto_insert, only_test
from src.infra.db.common import is_test_mode
from src.infra.db.peewee.client import PeeweeTable


@pytest.mark.parametrize(
    "work_mode",
    list(common.WorkMode)
)
def test_only_test(mocker, work_mode):
    """
    設定されてた環境変数でonly_testが機能するかの確認
    """
    # ワークモードを強制変更
    mocker.patch(
        "src.infra.db.common.CURRENT_WORK_MODE",
        work_mode
    )
    """
    ワークモードが変更されているかを確認。
    パッチの影響を確認するにはfromからもののではなく、
    importしたものから直接確認が必要。

    # NOTE: patchしたモジュールをfromとimportによってインポートした場合の違い
        patchを当てたとしてもfromによってインポートした変数は変更されない。
        patchはモジュール側の値を書き換える。
        だがfromはモジュール側からのコピーをローカルに作る動作をするので、パッチの影響を受けない。
    """
    assert work_mode is common.CURRENT_WORK_MODE
    # デコレータ検証用関数
    @only_test
    def _f():
        return True
    """
    デコレータが機能しているかを確認

    # NOTE: is_test_mode()はなぜfromからなのに期待通りに動作しているのか？
        fromはモジュールからのコピーがローカルから作られる。
        だがコピーとはいえその関数が参照する値というのはモジュール内の値。
        つまりパッチにより書き換わった値を参照しているので期待通りpatchedな動作となる。
    """
    if is_test_mode():
        # テストモード状態であれば、関数_fは正常に実行される
        assert _f()
    else:
        # テストモード状態でなければ、関数_fはValueErrorで阻まれ実行されない
        with pytest.raises(ValueError, match="EID:019d3665"):
            _f()


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
