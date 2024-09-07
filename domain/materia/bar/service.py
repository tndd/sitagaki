from datetime import datetime

from domain.materia.bar.repository import BarRepository


def fetch_bars(
        rp: BarRepository,
        symbol: str,
        start: datetime = datetime(2000,1,1),
        end: datetime = datetime.now()
    ):
    """
    条件:
        シンボルと開始日、終日を指定。
    戻り値:
        DF
    効果:
        対象期間のローソク足をDBから取得し保存する。
        もしもDBにデータが存在しなければ、オンライン上からの取得を試みる。
    """
    # IMPL
    pass


def update_bars(
        date_to: datetime = datetime.now()
    ):
    """
    条件:
        何日地点までアップデートするかの日時。
    効果:
        データベースのbar情報を最新の状態に更新する。
    """
    # IMPL
    pass


def fetch_latest_date_of_symbol(symbol: str) -> str:
    """
    指定シンボルの最新のデータの日付を取得する。
    """
    # IMPL
    pass


def update_bars_of_symbol(symbol: str, date_to: str):
    """
    条件:
        - 更新対象のシンボル
        - 何日まで更新するかの日付
    効果:
        指定シンボルのデータベース上のbar情報を更新する
    """
    # IMPL
    pass