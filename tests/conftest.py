import sys
from pathlib import Path

from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest

# テスト用fixture
from tests.utils.fixture.domain.materia.finance.chart import (
    mock_test_chart_repo,
    mock_test_chart_repo_failed_api,
)
from tests.utils.fixture.infra.api.alpaca.bar import (
    mock_get_barset_alpaca_api,
    mock_get_barset_alpaca_api_empty_barset,
)
from tests.utils.fixture.infra.db.peewee import test_peewee_cli
from tests.utils.fixture.infra.db.table.bar import prepare_table_bar_alpaca_on_db


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    pass
