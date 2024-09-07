import sys
from pathlib import Path

# 環境変数の読み込み
load_dotenv()
# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

from infra.db.sqlmodel import SQLModelClient
from tests.utils.fixture.materia.bar import test_bar_repo


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    pass


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def test_sqlm_cli(test_engine):
    return SQLModelClient(test_engine)
