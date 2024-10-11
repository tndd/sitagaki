import pytest

import src.infra.db.common
from fixture.decorator import only_test
from src.infra.db.common import CURRENT_WORK_MODE, WorkMode, is_test_mode

print(f"Contents of src.infra.db.common: {dir(src.infra.db.common)}")
print(f"CURRENT_WORK_MODE in src.infra.db.common: {'CURRENT_WORK_MODE' in dir(src.infra.db.common)}")
if 'CURRENT_WORK_MODE' in dir(src.infra.db.common):
    print(f"Value of CURRENT_WORK_MODE: {src.infra.db.common.CURRENT_WORK_MODE}")
    print(f"Value of CURRENT_WORK_MODE(from): {CURRENT_WORK_MODE}")


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
        work_mode
    )
    print('=================')
    print(f"After patch - Value of CURRENT_WORK_MODE: {src.infra.db.common.CURRENT_WORK_MODE}")
    print(f"After patch - Value of CURRENT_WORK_MODE(from): {CURRENT_WORK_MODE}")
    # CURRENT_WORK_MODE = work_mode # HACK: これを追加するとなぜかテスト期待通りの動作となる
    print('=================')
    print(f"is_test_mode: {src.infra.db.common.is_test_mode()}")
    print(f"is_test_mode(from): {is_test_mode()}")
    # ワークモードが変更されているかを確認
    assert work_mode is src.infra.db.common.CURRENT_WORK_MODE
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
