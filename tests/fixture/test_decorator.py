import pytest

import src.infra.db.common as common
from fixture.decorator import only_test
from src.infra.db.common import is_test_mode


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
