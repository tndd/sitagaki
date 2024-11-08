from datetime import datetime

from loguru import logger


def get_logger(
    path: str = f"log/data/{datetime.now().strftime('%Y/%m/%d')}.log"
):
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


LOG = get_logger()