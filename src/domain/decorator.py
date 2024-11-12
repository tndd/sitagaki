from contextlib import contextmanager

from log.client import LOG, build_payload


@contextmanager
def log_error(
    message: str,
    extra: dict = {},
):
    """
    失敗時に引数のメッセージとエラーの内容から、
    ログを作成し記録する。
    """
    try:
        yield
    except Exception as e:
        """
        TODO: localsの中身
            本当は呼び出し側のlocals()の結果が欲しいが、
            このままではこのlog_errorのlocals()が呼び出されてしまう。
        """
        payload = build_payload(
            payload={
                '__locals__': locals(),
                '__extra__': extra,
            },
            exception=e
        )
    LOG.error(message, **payload)
