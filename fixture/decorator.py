import pytest
from decorator import decorator

from src.infra.db.common import is_test_mode


@decorator
def test_only(f, *args, **kwargs):
    """
    テストモード以外で実行するとエラーを吐き強制終了させるデコレータ。
    """
    if not is_test_mode():
        raise ValueError("テストモードではないため、実行できません。")
    return f(*args, **kwargs)
