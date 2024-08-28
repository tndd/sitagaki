from infra.db.table.alpaca import TblBarDay, TblBarHour, TblBarMin

"""
# Note: 作業メモ

とりあえずテーブルができているかの確認だけでもするか？
本当はデータの挿入や確認というテストが必要だが、
そのためにはまずBarモデルをTblBar*に変換するアダプタを用意しないと。
それとBarのfactoryも。
"""

def test_tbl_bar_min(test_sqlm_cli):
    pass


def test_tbl_bar_hour(test_sqlm_cli):
    pass


def test_tbl_bar_day(test_sqlm_cli):
    pass