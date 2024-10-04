from enum import Enum

from peewee import CharField, CompositeKey, DateTimeField, FloatField
from peewee_enum_field import EnumField

from infra.db.peewee.table.base import PeeweeTable


class TimeframeTable(Enum):
    MIN = 1
    HOUR = 2
    DAY = 4
    WEEK = 8
    MONTH = 16


class AdjustmentTable(Enum):
    RAW = 1
    SPLIT = 2
    DIVIDEND = 4
    ALL = 8


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
    timeframe = EnumField(TimeframeTable)
    adjustment = EnumField(AdjustmentTable)
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = FloatField()
    trade_count = FloatField(null=True)
    vwap = FloatField(null=True)

    class Meta:
        table_name = "alpaca_bar"
        primary_key = CompositeKey('timestamp', 'symbol', 'timeframe', 'adjustment')
