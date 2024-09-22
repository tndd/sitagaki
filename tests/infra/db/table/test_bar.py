from infra.db.table.bar import AdjustmentAlpaca, TblBarAlpaca, TimeframeAlpaca

"""
# Note: テーブルテストの実装方針

とりあえずテーブルができているかの確認だけでもするか？
本当はデータの挿入や確認というテストが必要だが、
そのためにはまずBarモデルをTblBar*に変換するアダプタを用意しないと。
それとBarのfactoryも。
"""

def test_tbl_bar(test_sqlm_cli):
    """
    AdjustmentAlpacaとTimeframeAlpacaを渡した際、
    正常にTblBarAlpacaが生成されることを確認する。
    """
    pass
