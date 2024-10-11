import pytest
from alpaca.trading.models import Asset

from src.infra.api.alpaca.trade import get_assets


@pytest.mark.online_slow
def test_get_assets():
    assets = get_assets()
    assert isinstance(assets, list)
    assert all(isinstance(asset, Asset) for asset in assets)