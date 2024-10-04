import sys
from pathlib import Path

from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest

# テスト用fixture
from tests.utils.fixture.clear import cleanup_for_test
from tests.utils.fixture.load import load_table_bar_alpaca_on_db
from tests.utils.fixture.patch import (
    patch_with_mock_get_barset_alpaca_api,
    patch_with_mock_get_barset_alpaca_api_fail_empty_barset,
)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    pass


@pytest.fixture(scope="function", autouse=True)
def setup_function():
    cleanup_for_test()
