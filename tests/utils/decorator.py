import pytest
from decorator import decorator

from infra.db.common import is_test_mode


@pytest.mark.skip # 基本的にこのファイルはテスト対象にはならないが念の為
@decorator
def test_only(f, *args, **kwargs):
    """
    テストモード以外で実行するとエラーを吐き強制終了させるデコレータ。
    """
    if not is_test_mode():
        raise ValueError("テストモードではないため、実行できません。")
    return f(*args, **kwargs)
