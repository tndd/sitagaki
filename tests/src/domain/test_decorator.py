from log.client import read_log_latest_line
from src.domain.decorator import log_error

"""
TODO: テスト拡充
    もっとログの中身を詳細にassertする。
"""


def test_log_error():
    """
    ゼロ除算によるエラーを発生させた際、
    ログへの記録が自動的に行われていることを確認
    """
    error_id = '7d0b8f29'
    with log_error(error_id):
        1 / 0
    log = read_log_latest_line()
    assert error_id in log