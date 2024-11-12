from contextlib import contextmanager

from log.service import LOG, build_payload


@contextmanager
def log_error(
    message: str,
    payload: dict = {},
):
    """
    失敗時に引数のメッセージとエラーの内容から、
    ログを作成し記録する。

    payloadは値の記録が必要な場合に使う。
    """
    try:
        yield
    except Exception as e:
        payload = build_payload(
            payload,
            exception=e
        )
    LOG.error(message, **payload)
