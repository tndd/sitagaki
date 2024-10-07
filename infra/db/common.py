from enum import Enum
from os import getenv
from typing import Final


class WorkMode(Enum):
    """
    DBの動作モードを表す
    """
    TEST = 'TEST'
    DEV = 'DEV'
    PROD = 'PROD'
    IN_MEMORY = 'IN_MEMORY'


def read_work_mode_from_env() -> WorkMode:
    """
    環境変数からワークモードを決定する。
    "WORK_MODE"という環境変数名を指定しておくこと。

    環境変数が指定されていない場合は、IN_MEMORYを返す。
    """
    env_work_mode = getenv('WORK_MODE', 'NO_SET')
    if env_work_mode == 'TEST':
        work_mode = WorkMode.TEST
    elif env_work_mode == 'DEV':
        work_mode = WorkMode.DEV
    elif env_work_mode == 'PROD':
        work_mode = WorkMode.PROD
    elif env_work_mode == 'IN_MEMORY' or env_work_mode == 'NO_SET':
        # 環境変数未指定時についてもIN_MEMORYを返す
        work_mode = WorkMode.IN_MEMORY
    else:
        raise ValueError(f"指定されたワークモードは存在しません: {env_work_mode}")
    return work_mode

# ワークモードは不可逆的に決定される
CURRENT_WORK_MODE: Final[WorkMode] = read_work_mode_from_env()


def is_test_mode() -> bool:
    """
    テストモードまたはインメモリモードかどうかを返す
    """
    return CURRENT_WORK_MODE in (
        WorkMode.TEST,
        WorkMode.IN_MEMORY,
    )
