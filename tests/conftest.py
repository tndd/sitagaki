import sys
from pathlib import Path

from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import socket
from os import environ

import pytest

from tests.utils.operate.danger import cleanup_tables

# テスト用fixture
from tests.utils.patch.api.alpaca.bar import (
    fx_replace_patch_alpaca_get_stock_bars_empty,
    patch_alpaca_get_stock_bars,
)


@pytest.fixture(scope="session", autouse=True)
def setup_session(session_mocker):
    # 環境変数WorkModeをテスト仕様に強制する
    environ['WORK_MODE'] = 'IN_MEMORY'


@pytest.fixture(scope="function", autouse=True)
def setup_function(request, mocker):
    """
    各テスト開始時に実行されるfixture
    """
    # データの初期化
    cleanup_tables()
    # 通信関数のモック化
    patch_alpaca_get_stock_bars(mocker)
    # マーカーごとの特別処理
    if request.node.get_closest_marker('online') \
        or request.node.get_closest_marker('online_slow'):
        # onlineテストではモックを一時的に無効化する
        mocker.stopall()
    yield


@pytest.fixture
def airplane_mode():
    """
    # LATER: まだ正常に機能してない

    このフィクスチャを適応したテストの通信は、
    強制的に遮断状態となる。
    """
    original_socket = socket.socket
    def blocked_socket(*args, **kwargs):
        raise OSError("通信は遮断されています（機内モード発動中）")
    socket.socket = blocked_socket
    try:
        yield
    finally:
        socket.socket = original_socket