from os import getenv
from typing import List

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass
from alpaca.trading.models import Asset
from alpaca.trading.requests import GetAssetsRequest

cli_trading = TradingClient(
    api_key=getenv('APCA_KEY'),
    secret_key=getenv('APCA_SECRET')
)

def get_assets() -> List[Asset]:
    """
    全ての株式のリストを取得する。
    """
    search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
    return cli_trading.get_all_assets(search_params)