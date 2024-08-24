import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    # 環境変数の読み込み
    load_dotenv()


