from uuid import UUID

from pydantic import BaseModel


class Ticker(BaseModel):
    """
    TODO: フィールド内容検討
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