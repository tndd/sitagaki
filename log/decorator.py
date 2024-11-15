"""
TODO: デコレータ廃止？
    デコレータでログを吐く機能自体を一元的に管理しようとした場合、
    どうしてもログ内容と吐き場所に乖離が生じてしまう。

    ログが必要な箇所側でログ内容をある程度構築するという手順は、
    避けては通れないのかもしれない。

    idea:
        * ログの書式自体に汎用性を持たせる？
        * いっそmessageに必要な最低限のログ情報を詰め込ませる？
        * エラー機能は集約するが、エラー箇所の特定にはIDを使うことで対応するか？
"""


from contextlib import contextmanager

from log.service import LOG, build_payload


@contextmanager
def log_error(
    message: str,
    locals: dict = {},
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
            locals=locals,
            exception=e
        )
    LOG.error(message, **payload)
