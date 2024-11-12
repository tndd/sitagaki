from log.client import LOG, build_payload, read_log


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
    log.info('これは情報メッセージです', **{"user": "info", "action": "login"})
    log.debug('これはデバッグメッセージです', **{"user": "debug", "action": "login"})
    log.warning('これは警告メッセージです', **{"user": "warning", "action": "login"})
    log.error('これはエラーメッセージです', **{"user": "error", "action": "login"})
    # ログの検証
    with open(TEST_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # ログは４件保存されている
        assert len(lines) == 4
        # 各ログメッセージの内容を検証（任意で追加）
        assert "これは情報メッセージです" in lines[0]
        assert "これはデバッグメッセージです" in lines[1]
        assert "これは警告メッセージです" in lines[2]
        assert "これはエラーメッセージです" in lines[3]
        # 各ログメッセージのpayload部分を検証
        assert "{'user': 'info', 'action': 'login'}" in lines[0]
        assert "{'user': 'debug', 'action': 'login'}" in lines[1]
        assert "{'user': 'warning', 'action': 'login'}" in lines[2]
        assert "{'user': 'error', 'action': 'login'}" in lines[3]


def test_build_payload():
    """
    exception発生時のログについての確認
    """
    def calc(x, y):
        return x / y

    clear_log(TEST_PATH)
    try:
        # ゼロ除算によるエラー
        calc(1, 0)
    except Exception as e:
        payload = build_payload(
            payload={'p_key': 'p_value'},
            exception=e
        )
        log.error('zero div', **payload)
    # ログ検証
    with open(TEST_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # メッセージ
        assert 'zero div' in lines[0]
        # ペイロード
        assert "'p_key': 'p_value'" in lines[0]
        # 例外オブジェクト
        assert "'__exception__': {'class': 'ZeroDivisionError', 'args': ('division by zero',)}" in lines[0]
