from infra.adapter.materia.bar import (adapt_to_bar_list,
                                       adapt_to_tbl_bar_alpaca)
from tests.utils.factory.infra.alpaca import MockBar, generate_barset_mock


def test_adapt_to_bar_list():
    mock_barset = generate_barset_mock()
    bars = adapt_to_bar_list(mock_barset)
    assert isinstance(bars, list)
    """
    # WARN: 擬似テスト

    MockBarについて:
        * MockBarはalpacaのBarとは継承関係にないクラス。
        * 本家のBarモデルの作成が困難であるためモックを使っている。
        * しかしMockBarはBarの要素を全て保有している。
        * このアダプタの変換テストにはモックであっても支障はない。
    """
    assert all(isinstance(bar, MockBar) for bar in bars)


def test_adapt_to_tbl_bar_alpaca():
    pass