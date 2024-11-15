from dataclasses import dataclass
from datetime import datetime
from distutils.command import build
from typing import Sequence

from log.decorator import log_error
from log.service import LOG, build_payload
from src.domain.origin.alpaca.bar.const import Adjustment, Timeframe
from src.domain.origin.alpaca.bar.model import Chart, SymbolTimestampSet
from src.infra.adapter.origin.alpaca.bar import (
    arrive_chart_from_bar_alpaca_api_list,
    arrive_chart_from_table_list,
    arrive_symbol_timestamp_dict_from_table,
    depart_adjustment_to_alpaca_api,
    depart_adjustment_to_table,
    depart_chart_to_table_list,
    depart_timeframe_to_alpaca_api,
    depart_timeframe_to_table,
)
from src.infra.api.alpaca.bar import AlpacaApiBarClient
from src.infra.db.peewee.client import CLI_PEEWEE, PeeweeClient
from src.infra.db.peewee.query.origin.alpaca.bar import (
    get_query_bar_alpaca,
    get_query_latest_timestamps,
)


@dataclass
class ChartRepository:
    cli_db: PeeweeClient
    cli_alpaca: AlpacaApiBarClient

    def store_chart_from_online(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: datetime | None = None,
        limit: int | None = None
    ) -> None:
        """
        指定されたシンボルのbarデータをonlineから取得し、DBに保存する。

        NOTE: endの指定がない理由
            基本的にオンライン上からデータを取得する場合、最新の日付までのデータを求めるから。
            endを指定したデータ取得の必要性を感じないし、いらない部分があるなら捨てればいい。
        """
        try:
            # barsデータを取得
            bar_alpaca_api_list = self.cli_alpaca.get_bar_alpaca_api_list(
                symbol=symbol,
                timeframe=depart_timeframe_to_alpaca_api(timeframe),
                adjustment=depart_adjustment_to_alpaca_api(adjustment),
                start=start,
                limit=limit
            )
        except Exception as e:
            payload = build_payload(
                conditon={
                    'symbol': symbol,
                    'timeframe': timeframe.value,
                    'adjustment': adjustment.value,
                    'start': str(start)
                },
                exception=e
            )
            LOG.error('Alpaca api通信部分で失敗', **payload)
        # adapt: <= alpaca_api
        chart = arrive_chart_from_bar_alpaca_api_list(
            bars_alpaca_api=bar_alpaca_api_list,
            adjustment=adjustment,
            timeframe=timeframe
        )
        # adapt: => peewee_table
        bar_table_list = depart_chart_to_table_list(chart)
        # DBのモデルリストを保存
        self.cli_db.insert_models(bar_table_list)
        LOG.info(f'オンラインからDBへ保存完了。 symbol={symbol},{timeframe},{adjustment},start={start}')

    def fetch_chart_from_local(
        self,
        symbol: str,
        timeframe: Timeframe,
        adjustment: Adjustment,
        start: datetime | None = None,
        end: datetime | None = None
    ) -> Chart:
        """
        ローカルのDBから指定されたシンボルのbarを取得する。

        不足データをオンラインから取得するみたいな気の利いた動作はさせていない。
        """
        conditon={
            'symbol': symbol,
            'timeframe': timeframe.value,
            'adjustment': adjustment.value,
            'start': str(start),
            'end': str(end)
        }
        # 取得に必要なqueryを作成
        query = get_query_bar_alpaca(
            symbol=symbol,
            timeframe=depart_timeframe_to_table(timeframe),
            adjustment=depart_adjustment_to_table(adjustment),
            start=start,
            end=end
        )
        try:
            # TableBarAlpacaのリストを取得
            bar_list_table = self.cli_db.exec_query_fetch(query)
        except Exception as e:
            payload = build_payload(
                conditon=conditon,
                exception=e
            )
            LOG.error('DBからの情報取得部分で失敗', **payload)
        if not bar_list_table:
            # 取得件数が0の場合、警告ログを残して空のChartを返す
            LOG.warning('Barの取得件数が0件。おそらく条件指定が間違っている', **conditon())
            return Chart(
                symbol=symbol,
                timeframe=timeframe,
                adjustment=adjustment,
                bars = []
            )
        # 取得物をドメイン層のbarモデルのリストに変換して返す
        return arrive_chart_from_table_list(bar_list_table)

    def fetch_latest_symbol_timestamp_set(
        self,
        timeframe: Timeframe,
        adjustment: Adjustment,
        symbols: Sequence[str] | None = None,
    ) -> SymbolTimestampSet:
        """
        指定されたtimeframe,adjustment,symbolsの条件の、
        DB上のシンボルについての最新のtimestampを返す。

        > 未取得のシンボルについて
            timestamp=Noneとして返す
        """
        # シンボルごとの最新日付取得
        query = get_query_latest_timestamps(
            symbols=symbols,
            timeframe=depart_timeframe_to_table(timeframe),
            adjustment=depart_adjustment_to_table(adjustment)
        )
        try:
            model_talbe_ls = self.cli_db.exec_query_fetch(query)
        except Exception as e:
            payload = build_payload(
                conditon={
                    'timeframe': timeframe.value,
                    'adjustment': adjustment.value,
                    'symbols': str(symbols)
                },
                exception=e
            )
            LOG.error('DBからの情報取得部分で失敗', **payload)
        # 取得したシンボルと日付のペアを辞書へ変換。
        # \ 存在しない日付のtimestampはNoneに置き換え。
        symbol_timestamp_dc = arrive_symbol_timestamp_dict_from_table(
            symbols=symbols,
            tables=model_talbe_ls
        )
        return SymbolTimestampSet(
            timeframe=timeframe,
            adjustment=adjustment,
            data=symbol_timestamp_dc
        )


# Singleton
REPO_CHART = ChartRepository(
    cli_db=CLI_PEEWEE,
    cli_alpaca=AlpacaApiBarClient()
)
