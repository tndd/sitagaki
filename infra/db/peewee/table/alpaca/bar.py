from enum import Enum

from peewee import CharField, CompositeKey, DateTimeField, FloatField
from peewee_enum_field import EnumField

from infra.db.peewee.client import PeeweeTable


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
