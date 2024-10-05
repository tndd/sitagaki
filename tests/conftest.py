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
from tests.utils.fixture.patch import (
    patch_with_mock_get_barset_alpaca_api,
    patch_with_mock_get_barset_alpaca_api_fail_empty_barset,
)


@pytest.fixture(scope="session", autouse=True)
def setup_session(session_mocker):
    """
    データベースの初期化
        セッション開始時はデータベースが初期化された状態にする。
    """
    """
    全通信部分をモック化
        通信機能が実装されている箇所のみパッチを打ち消す形で、
        部分的にオンラインテストを実行する形式とする。
    """
    patch_with_mock_get_barset_alpaca_api(session_mocker)
    yield


@pytest.fixture(scope="function", autouse=True)
def setup_function():
    """
    各テスト開始時に実行されるfixture

    データベースの初期化
        各関数開始時にもデータベースは完全に初期化する。

    # FIXME: onlineマーカーの際にはモックを無効化する処理追加
    """
    cleanup_for_test()
    yield
