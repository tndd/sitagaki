import sys
from pathlib import Path

from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
# プロジェクトルートへのパス通し
sys.path.append(str(Path(__file__).resolve().parent.parent))

import socket

import pytest

import infra.db.peewee.client as peewee_cli

# テスト用fixture
from tests.utils.patch.api.alpaca.bar import (
    fx_replace_with_mock_get_barset_alpaca_api_fail_empty_barset,
    patch_with_mock_get_barset_alpaca_api,
)


@pytest.fixture(scope="session", autouse=True)
def setup_session(session_mocker):
    pass


@pytest.fixture(scope="function", autouse=True)
def setup_function(request, mocker):
    """
    各テスト開始時に実行されるfixture
    """
    # データの初期化
    peewee_cli.cleanup_tables('DELETE_ALL')
    # 通信関数のモック化
    patch_with_mock_get_barset_alpaca_api(mocker)
    # マーカーごとの特別処理
    if request.node.get_closest_marker('online'):
        # onlineテストではモックを一時的に無効化する
        mocker.stopall()
    yield


@pytest.fixture
def airplane_mode():
    """
    # TODO: まだ正常に機能してない

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