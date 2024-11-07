from log.client import CLI_LOG


def test_basic():
    """
    基本的な一連のログ保存を検証
    payload無しの単純なメッセージのみの動作確認
    """
    CLI_LOG.info('これは情報メッセージです')
    CLI_LOG.debug('これはデバッグメッセージです')
    CLI_LOG.warn('これは警告メッセージです')
    CLI_LOG.err('これはエラーメッセージです')
    # ログの検証
    with open(CLI_LOG.log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # ログは４件保存されている
        assert len(lines) == 4
        # 各ログメッセージの内容を検証（任意で追加）
        assert "これは情報メッセージです" in lines[0]
        assert "これはデバッグメッセージです" in lines[1]
        assert "これは警告メッセージです" in lines[2]
        assert "これはエラーメッセージです" in lines[3]
