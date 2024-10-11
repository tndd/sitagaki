import pytest

from tests.utils.patch.api.alpaca.bar import patch_get_stock_bars_empty


@pytest.fixture
def fx_replace_api_alpaca_get_stock_bars_empty(mocker):
    patch_get_stock_bars_empty(mocker)