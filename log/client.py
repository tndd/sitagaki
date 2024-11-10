from datetime import datetime

from loguru import logger

from common.workmode import CURRENT_WORK_MODE

# ログの吐き先はワークモードによって変わる
_log_dir = CURRENT_WORK_MODE.value.lower()


def get_logger(
    path: str = f"log/{_log_dir}/{datetime.now().strftime('%Y/%m/%d')}.log"
):
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


def build_payload(payload: dict, exception: Exception | None):
    """
    payloadに例外オブジェクトの情報を追加して返す
    """
    if exception:
        payload['__exception__'] = {
            'class': str(exception.__class__.__name__),
            'args': exception.args
        }
    return payload


# 基本的には、このLOGをインポートする形でログ機能を利用する。
LOG = get_logger()