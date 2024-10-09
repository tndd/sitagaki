from datetime import datetime
from os import getenv

from alpaca.data.historical import StockHistoricalDataClient

# データ取得のデフォルトの開始時刻
ROOT_START_DATETIME = datetime(2000, 1, 1)
# APIの仕様上、15分前の時刻まではendを指定できる
DELAY = 15

historical_cli = StockHistoricalDataClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)