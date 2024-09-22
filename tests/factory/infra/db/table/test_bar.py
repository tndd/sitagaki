from infra.db.table.bar import AdjustmentAlpaca, TblBarAlpaca, TimeframeAlpaca
from tests.utils.factory.infra.db.table.bar import generate_tbl_bar_alpaca


def test_generate_tbl_bar_alpaca():
    """
    組み合わせテスト
    timeframeとadjustmentのすべての組み合わせを検証する
    """
    for timeframe in TimeframeAlpaca:
        for adjustment in AdjustmentAlpaca:
            # モデル作成部分
            tbl_bar_alpaca = generate_tbl_bar_alpaca(timeframe, adjustment)
            # モデルの中身のチェック
            assert isinstance(tbl_bar_alpaca, TblBarAlpaca)
            assert tbl_bar_alpaca.timeframe == timeframe
            assert tbl_bar_alpaca.adjustment == adjustment


# WARN: ↓ tbl_bar_alpacaのテスト完了次第、このコメントアウトを取り消す。
# def test_generate_tbl_bar_base_list():
#     tbl_bar_base_list = generate_tbl_bar_base_list()
#     assert isinstance(tbl_bar_base_list, list)
#     assert all(isinstance(tbl_bar_base, TblBarBase) for tbl_bar_base in tbl_bar_base_list)
