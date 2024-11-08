from datetime import datetime

from loguru import logger

"""
TODO: ログの吐き先
    今の状態ではテスト環境のものも本番のものも、
    日付については分かれているが、すべて同じところに吐かれてしまう。
    test,dev,prdの３つの動作環境ごとにログの吐き先は変える
"""


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