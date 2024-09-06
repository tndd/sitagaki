from infra.db.table.bar import (TblBarDayAlpaca, TblBarHourAlpaca,
                                TblBarMinAlpaca)

"""
# TODO: テーブルテストの実装方針

とりあえずテーブルができているかの確認だけでもするか？
本当はデータの挿入や確認というテストが必要だが、
そのためにはまずBarモデルをTblBar*に変換するアダプタを用意しないと。
それとBarのfactoryも。
"""

def test_tbl_bar_min_alpaca(test_sqlm_cli):
    pass


def test_tbl_bar_hour_alpaca(test_sqlm_cli):
    pass


def test_tbl_bar_day_alpaca(test_sqlm_cli):
    pass