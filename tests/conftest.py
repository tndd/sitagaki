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

"""
FIXME: monkeypatchに切り替え
    mockerでは想定される動作を実現できていない。
    パッチ化したはずの関数が一部でパッチ化されていない現象が発生している。
    パッチ化した関数を直接呼び出した際に問題が起こるようだ。
"""


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
    peewee_cli.cleanup_tables('DELETE_ALL')
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