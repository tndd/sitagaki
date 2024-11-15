from datetime import datetime

from loguru import logger

from common.workmode import CURRENT_WORK_MODE
from fixture.decorator import only_test

# ログの吐き先はワークモードによって変わる
_log_dir = CURRENT_WORK_MODE.value.lower()
_log_path = f"log/{_log_dir}/{datetime.now().strftime('%Y/%m/%d')}.log"


def get_logger(path: str = _log_path):
    """
    ワークモードごとにログは独立している。
    ログディレクトリは'年/月/日付.log'という単位で更新される形式。

    NOTE: get_loggerの利用について
        この関数は原則として外部からは呼ばれない。
        ログ機能を利用する際には下部に定義されているLOGをインポートする。

        ただしテストなどでログを部分的に複製したいという特別な用途において、
        この関数が利用されることはあり得る。
    """
    logger.add(
        path,
        format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {file.path} | {function} | {message} | {extra}",
        encoding='utf-8'
    )
    return logger


def build_payload(
    payload: dict,
    exception: Exception | None
):
    """
    payloadに例外オブジェクトの情報を追加して返す
    """
    if exception:
        payload['__exception__'] = {
            'class': str(exception.__class__.__name__),
            'args': exception.args
        }
    return payload


def read_log():
    """
    現在の吐き先ログファイルの全体を読み込む
    """
    with open(_log_path, 'r') as f:
        return f.readlines()


def read_log_latest_line():
    """
    吐き先ログファイルの直近一行を読み込む
    """
    lines = read_log()
    return lines[-1]


@only_test
def clear_log():
    """
    ログをクリアする。
    危険な関数なのでテスト環境以外では実行できないようにしておく。
    """
    with open(_log_path, 'w') as f:
        f.truncate(0)


# 基本的には、このLOGをインポートする形でログ機能を利用する。
LOG = get_logger()