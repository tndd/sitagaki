from log.client import LogClient

# テスト用にログパスを特別に変更している
TEST_LOG_PATH ='log/data/test.log'
cli = LogClient(log_path=TEST_LOG_PATH)


def test_basic():
    """
    基本的な一連のログ保存を検証
    payload無しの単純なメッセージのみの動作確認
    """
    # ログをクリアしておく
    clear_log(cli.log_path)
    cli.info('これは情報メッセージです')
    cli.debug('これはデバッグメッセージです')
    cli.warn('これは警告メッセージです')
    cli.err('これはエラーメッセージです')
    # ログの検証
    with open(cli.log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # ログは４件保存されている
        assert len(lines) == 4
        # 各ログメッセージの内容を検証（任意で追加）
        assert "これは情報メッセージです" in lines[0]
        assert "これはデバッグメッセージです" in lines[1]
        assert "これは警告メッセージです" in lines[2]
        assert "これはエラーメッセージです" in lines[3]


def test_with_payload():
    """
    payloadありのログ機能を確かめる
    """
    clear_log(cli.log_path)
    cli.info('これは情報メッセージです', {"user": "example_user", "action": "login"})
    cli.debug('これはデバッグメッセージです', {"user": "example_user", "action": "login"})
    cli.warn('これは警告メッセージです', {"user": "example_user", "action": "login"})
    cli.err('これはエラーメッセージです', {"user": "example_user", "action": "login"})
    # ログの検証
    with open(cli.log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # ログは４件保存されている
        assert len(lines) == 4
        # 各ログメッセージの内容を検証（任意で追加）
        assert "これは情報メッセージです" in lines[0]
        assert "これはデバッグメッセージです" in lines[1]
        assert "これは警告メッセージです" in lines[2]
        assert "これはエラーメッセージです" in lines[3]
        # 各ログメッセージのpayload部分を検証
        assert "{'user': 'example_user', 'action': 'login'}" in lines[0]
        assert "{'user': 'example_user', 'action': 'login'}" in lines[1]
        assert "{'user': 'example_user', 'action': 'login'}" in lines[2]
        assert "{'user': 'example_user', 'action': 'login'}" in lines[3]


def clear_log(path):
    """
    指定パスのログファイルの中身を空にする
    """
    with open(path, 'w') as f:
        f.truncate(0)