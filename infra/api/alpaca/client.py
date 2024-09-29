from os import getenv

from alpaca.data.historical import StockHistoricalDataClient

historical_cli = StockHistoricalDataClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)