from os import environ

from infra.db.common import WorkMode, get_work_mode


def test_get_work_mode():
    """
    通常動作時にはIN_MEMORYを返すこと。
    """
    assert get_work_mode() == WorkMode.IN_MEMORY


def test_get_work_mode_with_env():
    """
    環境変数が指定されている場合はその値を返すこと。
    """
    environ['WORK_MODE'] = 'TEST'
    assert get_work_mode() == WorkMode.TEST
    environ['WORK_MODE'] = 'DEV'
    assert get_work_mode() == WorkMode.DEV
    environ['WORK_MODE'] = 'PROD'
    assert get_work_mode() == WorkMode.PROD
