from datetime import datetime

import pytest
from alpaca.trading.models import Asset
from loguru import logger

from infra.api.alpaca.trading import get_assets

# ログの設定
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_path = f"tests/logs/alpaca_assets_{current_time}.log"
logger.add(log_file_path)


# @pytest.mark.online
def test_get_assets():
    assets = get_assets()
    assert isinstance(assets, list)
    assert all(isinstance(asset, Asset) for asset in assets)
    # TSVヘッダーをログに記録
    header = "id\tasset_class\texchange\tsymbol\tname\tstatus\ttradable\tmarginable\tshortable\teasy_to_borrow\tfractionable\tmin_order_size\tmin_trade_increment\tprice_increment\tmaintenance_margin_requirement"
    logger.info(header)
    # assetsの内容をログに記録
    for asset in assets:
        log_line = f"{asset.id}\t{asset.asset_class}\t{asset.exchange}\t{asset.symbol}\t{asset.name}\t{asset.status}\t{asset.tradable}\t{asset.marginable}\t{asset.shortable}\t{asset.easy_to_borrow}\t{asset.fractionable}\t{asset.min_order_size}\t{asset.min_trade_increment}\t{asset.price_increment}\t{asset.maintenance_margin_requirement}"
        logger.info(log_line)
    # 取得したアセットの総数をログに記録
    logger.info(f"取得したアセットの総数: {len(assets)}")