from cgi import test
from datetime import datetime

from infra.db.table.bar import TableBarAlpaca


def test_table_bar_alpaca_is_created(test_peewee_cli):
    """
    bar_alpacaテーブルは作成されうるモデルであるかを確認。
    """
    # 投入用のTableBarAlpacaを作成
    table_bar_alpaca = TableBarAlpaca(
        symbol="AAPL",
        timestamp=datetime.now(),
        timeframe=1,
        adjustment=1,
        open=100.0,
        high=105.0,
        low=95.0,
        close=102.0,
        volume=1000,
        trade_count=100,
    )
    # テーブルに投入
    test_peewee_cli.insert_models([table_bar_alpaca])
    # テーブルの存在確認
    assert TableBarAlpaca.table_exists()
