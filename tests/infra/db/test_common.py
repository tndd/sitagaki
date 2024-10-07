import pytest

from infra.db.common import WorkMode, read_work_mode_from_env


def test_read_work_mode_from_env():
    """
    環境変数が指定されていない場合はIN_MEMORYを返すこと。
    """
    assert read_work_mode_from_env() == WorkMode.IN_MEMORY


@pytest.mark.parametrize("env_value, expected_mode", [
    ('TEST', WorkMode.TEST),
    ('DEV', WorkMode.DEV),
    ('PROD', WorkMode.PROD),
    ('IN_MEMORY', WorkMode.IN_MEMORY),
])
def test_read_work_mode_from_env_combination(env_value, expected_mode, monkeypatch):
    """
    環境変数が指定されている場合はその値を返すこと。
    """
    monkeypatch.setenv('WORK_MODE', env_value)
    assert read_work_mode_from_env() == expected_mode
