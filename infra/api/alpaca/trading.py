from os import getenv
from typing import List

from alpaca.trading.client import TradingClient
from alpaca.trading.models import Asset
from alpaca.trading.requests import GetAssetsRequest

cli_trading = TradingClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)

def get_assets() -> List[Asset]:
    """
    全てのtickerリストを取得する。

    Stock,Cryptoが含まれる。
    alpacaの仕様的には、Optionのものも将来的には含まれるようだ。
    """
    search_params = GetAssetsRequest()
    return cli_trading.get_all_assets(search_params)