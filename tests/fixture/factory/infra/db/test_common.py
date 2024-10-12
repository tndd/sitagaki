
from os import environ

import pytest

from src.infra.db.common import WorkMode, is_test_mode, read_work_mode_from_env


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
        "src.infra.db.common.CURRENT_WORK_MODE",
        work_mode
    )
    if work_mode in (WorkMode.TEST, WorkMode.IN_MEMORY):
        assert is_test_mode()
    else:
        assert not is_test_mode()
