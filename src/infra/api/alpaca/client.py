from datetime import datetime
from os import getenv

from alpaca.data.historical import StockHistoricalDataClient

# データ取得のデフォルトの開始時刻
ROOT_START_DATETIME = datetime(2000, 1, 1)


historical_cli = StockHistoricalDataClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)