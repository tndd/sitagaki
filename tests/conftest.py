import sys
from pathlib import Path

# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

from infra.db.sqlmodel import SqlModelClient


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    # 環境変数の読み込み
    load_dotenv()


@pytest.fixture
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def test_sqlm_cli(test_engine):
    return SqlModelClient(test_engine)