
from os import environ

import pytest

import common.workmode as workmode
from common.workmode import WorkMode, is_test_mode, only_test, read_work_mode_from_env


@pytest.mark.parametrize(
    "work_mode_env",
    ["TEST", "DEV", "PROD", "IN_MEMORY", "INVALID", ""]
)
def test_read_work_mode_from_env(mocker, work_mode_env):
    # 初期状態ではIN_MEMORYであることを確認
    assert read_work_mode_from_env() == WorkMode.IN_MEMORY
    # 環境変数をパッチ
    mocker.patch.dict(
        "os.environ",
        {"WORK_MODE": work_mode_env}
    )
    # 環境変数が上書きされたことを確認
    assert work_mode_env == environ["WORK_MODE"]
    # ワークモードに登録されている文字列であれば正常に実行され、対応するWorkModeが返る
    if work_mode_env in [mode.value for mode in WorkMode]:
        assert read_work_mode_from_env() == WorkMode[work_mode_env]
    else:
        # 未登録の環境変数であれば、ValueErrorが発生する
        with pytest.raises(ValueError):
            read_work_mode_from_env()


@pytest.mark.parametrize(
    "work_mode",
    list(WorkMode)
)
def test_is_test_mode(mocker, work_mode):
    # 初期状態ではテストモードであることを確認
    assert is_test_mode()
    # パッチ適用
    mocker.patch(
        "common.workmode.CURRENT_WORK_MODE",
        work_mode
    )
    if work_mode in (WorkMode.TEST, WorkMode.IN_MEMORY):
        assert is_test_mode()
    else:
        assert not is_test_mode()


@pytest.mark.parametrize(
    "work_mode",
    list(workmode.WorkMode)
)
def test_only_test(mocker, work_mode):
    """
    設定されてた環境変数でonly_testが機能するかの確認
    """
    # ワークモードを強制変更
    mocker.patch(
        "common.workmode.CURRENT_WORK_MODE",
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
    assert work_mode is workmode.CURRENT_WORK_MODE
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
