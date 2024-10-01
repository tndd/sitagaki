from peewee import BitField, CharField, CompositeKey, DateTimeField, FloatField

from infra.db.peewee.client import PeeweeTable


class TableBarAlpaca(PeeweeTable):
    """
    AlpacaのBarデータを保存するテーブル。

    保存容量を抑えるため、timeframeとadjustmentについては
    bitfieldを使用する。
        timeframe:
            * min = 1
            * hour = 2
            * day = 4
            * week = 8
            * month = 16
        adjustment:
            * raw = 1
            * split = 2
            * dividend = 4
            * all = 8
    """
    timestamp = DateTimeField()
    symbol = CharField()
    timeframe = BitField()
    adjustment = BitField()
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = FloatField()
    trade_count = FloatField(null=True)
    vwap = FloatField(null=True)

    class Meta:
        table_name = "bar_alpaca"
        primary_key = CompositeKey('timestamp', 'symbol', 'timeframe', 'adjustment')
