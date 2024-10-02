import sys
from pathlib import Path

from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest

# テスト用fixture
from tests.utils.fixture.domain.materia.stock.chart import (
    test_chart_repo_mocked_with_alpaca_api,
    test_chart_repo_with_alpaca_api_fail_empty_barset,
)
from tests.utils.fixture.infra.api.alpaca.bar import (
    replace_with_mock_get_barset_alpaca_api,
    replace_with_mock_get_barset_alpaca_api_fail_empty_barset,
)
from tests.utils.fixture.infra.db.peewee import test_peewee_cli
from tests.utils.fixture.infra.db.table.bar import prepare_table_bar_alpaca_on_db


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    pass
