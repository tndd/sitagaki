from enum import Enum
from os import getenv


class WorkMode(Enum):
    """
    DBの動作モードを表す
    """
    TEST = 'TEST'
    DEV = 'DEV'
    PROD = 'PROD'
    IN_MEMORY = 'IN_MEMORY'


def get_work_mode() -> WorkMode:
    """
    環境変数からワークモードを決定する。
    "WORK_MODE"という環境変数名を指定しておくこと。

    環境変数が指定されていない場合は、IN_MEMORYを返す。
    """
    env_work_mode = getenv('WORK_MODE', None)
    if env_work_mode == 'TEST':
        work_mode = WorkMode.TEST
    elif env_work_mode == 'DEV':
        work_mode = WorkMode.DEV
    elif env_work_mode == 'PROD':
        work_mode = WorkMode.PROD
    elif env_work_mode == 'IN_MEMORY' or env_work_mode is None:
        work_mode = WorkMode.IN_MEMORY
    return work_mode