import pytest

from infra.db.common import WorkMode, get_work_mode


def test_get_work_mode():
    """
    通常動作時にはIN_MEMORYを返すこと。
    """
    assert get_work_mode() == WorkMode.IN_MEMORY


@pytest.mark.parametrize("env_value, expected_mode", [
    ('TEST', WorkMode.TEST),
    ('DEV', WorkMode.DEV),
    ('PROD', WorkMode.PROD),
    ('IN_MEMORY', WorkMode.IN_MEMORY),
])
def test_get_work_mode_with_env(env_value, expected_mode, monkeypatch):
    """
    環境変数が指定されている場合はその値を返すこと。
    """
    monkeypatch.setenv('WORK_MODE', env_value)
    assert get_work_mode() == expected_mode
