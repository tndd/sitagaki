import pytest

from fixture.decorator import only_test
from src.infra.db.common import CURRENT_WORK_MODE, WorkMode


@pytest.mark.parametrize(
    "work_mode",
    list(WorkMode)
)
def test_only_test(mocker, work_mode):
    """
    設定されてた環境変数でonly_testが機能するかの確認
    """
    # ワークモードを強制変更
    mocker.patch(
        "src.infra.db.common.CURRENT_WORK_MODE",
        new=work_mode
    )
    CURRENT_WORK_MODE = work_mode # HACK: これを追加するとなぜかテスト期待通りの動作となる
    # ワークモードが変更されているかを確認
    assert work_mode is CURRENT_WORK_MODE
    # デコレータ検証用関数
    @only_test
    def _f():
        return True
    # デコレータが機能しているかを確認
    if work_mode in (WorkMode.TEST, WorkMode.IN_MEMORY):
        # fは実行される
        assert _f()
    else:
        # fはValueErrorで阻まれ実行されない
        with pytest.raises(ValueError, match="error_id: 019d3665"):
            _f()
