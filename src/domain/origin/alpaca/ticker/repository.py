from dataclasses import dataclass


@dataclass
class TickerRepository:
    data = {
        "dow": [
            "AMZN","AXP","AMGN","AAPL","BA","CAT","CSCO","CVX","GS","HD","HON","IBM","INTC","JNJ","KO","JPM","MCD","MMM","MRK","MSFT","NKE","PG","TRV","UNH","CRM","VZ","V","WMT","DIS","DOW"
        ],
        "sector": [
            "XLC","XLY","XLP","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLU"
        ]
    }

    def get_dow(self):
        return self.data['dow']

    def get_sector(self):
        return self.data['sector']


REPO_TICKER = TickerRepository()