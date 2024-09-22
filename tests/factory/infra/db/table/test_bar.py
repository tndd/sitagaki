from infra.db.table.bar import TblBarAlpaca
from tests.utils.factory.infra.db.table.bar import generate_tbl_bar_alpaca


def test_generate_tbl_bar_alpaca():
    tbl_bar_alpaca = generate_tbl_bar_alpaca()
    assert isinstance(tbl_bar_alpaca, TblBarAlpaca)


# WARN: ↓ tbl_bar_alpacaのテスト完了次第、このコメントアウトを取り消す。
# def test_generate_tbl_bar_base_list():
#     tbl_bar_base_list = generate_tbl_bar_base_list()
#     assert isinstance(tbl_bar_base_list, list)
#     assert all(isinstance(tbl_bar_base, TblBarBase) for tbl_bar_base in tbl_bar_base_list)
