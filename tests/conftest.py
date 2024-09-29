import sys
from pathlib import Path

from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest

# テスト用fixture
from tests.utils.fixture.domain.materia.bar import test_bar_repo
from tests.utils.fixture.infra.api.alpaca import (
    mock_get_barset_alpaca_api,
    mock_get_barset_alpaca_api_empty,
)
from tests.utils.fixture.infra.db.peewee import test_peewee_cli


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    pass
