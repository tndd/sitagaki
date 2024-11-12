from log.service import read_log_latest_line
from src.domain.decorator import log_error


def test_log_error():
    """
    ゼロ除算によるエラーを発生させた際、
    ログへの記録が自動的に行われていることを確認
    """
    error_id = '7d0b8f29'
    payload = {'locals': locals()}
    with log_error(error_id, payload):
        1 / 0
    log = read_log_latest_line()
    assert error_id in log
    assert '__exception__' in log
    assert "'locals': {" in log