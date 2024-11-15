from log.service import LOG, build_payload, read_log, read_log_latest_line


def test_basic():
    """
    基本的な一連のログ保存を検証
    payload無しの単純なメッセージのみの動作確認
    """
    # メッセージ一覧
    msg_info = 'info:00e19d1a'
    msg_debug = 'debug:7e356b40'
    msg_warning = 'warning:8a9b5dde'
    msg_error = 'error:88d8cd57'
    # ログ開始
    LOG.info(msg_info)
    LOG.debug(msg_debug)
    LOG.warning(msg_warning)
    LOG.error(msg_error)
    # ログの検証
    lines = read_log()
    assert msg_info in lines[-4]
    assert msg_debug in lines[-3]
    assert msg_warning in lines[-2]
    assert msg_error in lines[-1]


def test_with_payload():
    """
    payloadありのログ機能を確かめる
    """
    # メッセージ一覧
    msg_info = 'dfa1bd75'
    msg_debug = 'a1a1262d'
    msg_warning = '3970ff5a'
    msg_error = '1683302f'
    # Payload一覧
    payload_info = {"user": "info", "action": "login"}
    payload_debug = {"user": "debug", "action": "login"}
    payload_warning = {"user": "warning", "action": "login"}
    payload_error = {"user": "error", "action": "login"}
    # ログ開始
    LOG.info(msg_info, **payload_info)
    LOG.debug(msg_debug, **payload_debug)
    LOG.warning(msg_warning, **payload_warning)
    LOG.error(msg_error, **payload_error)
    # ログの検証
    lines = read_log()
    # 各ログメッセージの内容を検証
    assert msg_info in lines[-4]
    assert msg_debug in lines[-3]
    assert msg_warning in lines[-2]
    assert msg_error in lines[-1]
    # 各ログメッセージのpayload部分を検証
    assert str(payload_info) in lines[-4]
    assert str(payload_debug) in lines[-3]
    assert str(payload_warning) in lines[-2]
    assert str(payload_error) in lines[-1]



def test_build_payload():
    """
    exception発生時のログについての確認
    """
    def calc(x, y):
        return x / y

    try:
        a = 1
        b = 0
        # ゼロ除算によるエラー
        calc(a, b)
    except Exception as e:
        payload = build_payload(
            conditon={
                'a': a,
                'b': b
            },
            exception=e,
        )
        LOG.error('zero div', **payload)
    # ログ検証
    line = read_log_latest_line()
    # メッセージ
    assert 'zero div' in line
    # locals
    assert "{'__COND__': {'a': 1, 'b': 0}" in line
    # 例外オブジェクト
    assert "'__EXCP__'" in line
    # EXTRAは未指定であるから文字列内に含まれない
    assert not "'__EXTRA__'" in line
