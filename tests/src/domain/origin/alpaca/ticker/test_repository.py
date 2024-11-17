from src.domain.origin.alpaca.ticker.repository import REPO_TICKER


def test_get_dow():
    tickers = REPO_TICKER.get_dow()
    assert len(tickers) == 30
    assert tickers == ["AMZN","AXP","AMGN","AAPL","BA","CAT","CSCO","CVX","GS","HD","HON","IBM","INTC","JNJ","KO","JPM","MCD","MMM","MRK","MSFT","NKE","PG","TRV","UNH","CRM","VZ","V","WMT","DIS","DOW"]


def test_get_sector():
    tickers = REPO_TICKER.get_sector()
    assert len(tickers) == 11
    assert tickers == ["XLC","XLY","XLP","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLU"]
