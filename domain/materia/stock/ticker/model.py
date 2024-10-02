from enum import Enum

from pydantic import BaseModel


class Dow(Enum):
    AMZN = "Amazon.com Inc"
    AXP = "American Express Co"
    AMGN = "Amgen Inc"
    AAPL = "Apple Inc"
    BA = "Boeing Co"
    CAT = "Caterpillar Inc"
    CSCO = "Cisco Systems Inc"
    CVX = "Chevron Corp"
    GS = "Goldman Sachs Group Inc"
    HD = "Home Depot Inc"
    HON = "Honeywell International Inc"
    IBM = "International Business Machines Corp"
    INTC = "Intel Corp"
    JNJ = "Johnson & Johnson"
    KO = "Coca-Cola Co"
    JPM = "JPMorgan Chase & Co"
    MCD = "McDonald’s Corp"
    MMM = "3M Co"
    MRK = "Merck & Co Inc"
    MSFT = "Microsoft Corp"
    NKE = "Nike Inc"
    PG = "Procter & Gamble Co"
    TRV = "Travelers Companies Inc"
    UNH = "Unitedhealth Group Inc"
    CRM = "Salesforce Inc"
    VZ = "Verizon Communications Inc"
    V = "Visa Inc"
    WMT = "Walmart Inc"
    DIS = "Walt Disney Co"
    DOW = "Dow Inc"


class Sector(Enum):
    XLC = "Communication Services"
    XLY = "Consumer Discretionary"
    XLP = "Consumer Staples"
    XLE = "Energy"
    XLF = "Financials"
    XLV = "Health Care"
    XLI = "Industrials"
    XLB = "Materials"
    XLRE = "Real Estate"
    XLK = "Technology"
    XLU = "Utilities"


class Ticker(BaseModel):
    """
    LATER: フィールド内容検討
        これはドメイン層のモデルであるため、
        alpacaモデルをそのまま踏襲するのは良くない気もする。
        要素は必要最低限で抑えたい。
    """
    symbol: str
    name: str
    exchange: str
    asset_class: str
    status: str
    tradable: bool