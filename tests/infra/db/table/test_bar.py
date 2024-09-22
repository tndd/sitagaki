from sqlmodel import select

from infra.db.table.bar import AdjustmentAlpaca, TblBarAlpaca, TimeframeAlpaca
from tests.utils.factory.infra.db.table.bar import generate_tbl_bar_alpaca

"""
# Note: テーブルテストの実装方針

とりあえずテーブルができているかの確認だけでもするか？
本当はデータの挿入や確認というテストが必要だが、
そのためにはまずBarモデルをTblBar*に変換するアダプタを用意しないと。
それとBarのfactoryも。
"""

def test_tbl_bar(test_sqlm_cli):
    # sqlmモデル作成
    tbl_bar_alpaca = generate_tbl_bar_alpaca(
        timeframe=TimeframeAlpaca.MIN,
        adjustment=AdjustmentAlpaca.RAW
    )
    # sqlmをテーブルに書き込む
    test_sqlm_cli.insert_models([tbl_bar_alpaca])
    # テーブルからデータを取得
    stmt = select(TblBarAlpaca)
    result_models = test_sqlm_cli.exec_stmt(stmt)
    # 取得件数の確認
    assert len(result_models) == 1
    """
    timeframeとadjustmentは一致するか？
    """
    assert result_models[0].timeframe == tbl_bar_alpaca.timeframe
    assert result_models[0].adjustment == tbl_bar_alpaca.adjustment
