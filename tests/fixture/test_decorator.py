import pytest
from decorator import decorator

from src.infra.db.common import is_test_mode


def test_test_only():
    # TODO: テストモード以外の実行を阻止できているかを確認
    pass