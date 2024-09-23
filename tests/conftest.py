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
from tests.utils.fixture.infra.db.peewee import test_peewee_db
from tests.utils.fixture.infra.db.sqlmodel import test_engine, test_sqlm_cli


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    pass
