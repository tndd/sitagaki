
import pytest

from src.infra.db.common import WorkMode, is_test_mode


def test_read_work_mode_from_env():
    # TODO: 無指定状態でIN_MEMORYが返ること、そして全てのパターンのテスト
    pass


@pytest.mark.parametrize(
    "work_mode",
    list(WorkMode)
)
def test_is_test_mode(mocker, work_mode):
    # 初期状態ではテストモードであることを確認
    assert is_test_mode()
    # パッチ適用
    mocker.patch(
        "src.infra.db.common.CURRENT_WORK_MODE",
        work_mode
    )
    if work_mode in (WorkMode.TEST, WorkMode.IN_MEMORY):
        assert is_test_mode()
    else:
        assert not is_test_mode()
