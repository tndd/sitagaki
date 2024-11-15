from log.decorator import log_error
from log.service import read_log_latest_line


def test_log_error():
    """
    ゼロ除算によるエラーを発生させた際、
    ログへの記録が自動的に行われていることを確認
    """
    error_id = '7d0b8f29'
    with log_error(
        message=error_id,
        locals=locals(),
        payload={'payload': 'payload_data'}
    ):
        1 / 0
    log = read_log_latest_line()
    assert error_id in log
    assert '__exception__' in log
    assert '__locals__' in log
