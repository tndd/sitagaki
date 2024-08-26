from datetime import datetime

from domain.materia.bar.repository import BarRepository


def fetch_bars(
        rp: BarRepository,
        symbol: str,
        start: str = '2000-01-01',
        end: str = datetime.now().strftime('%Y-%m-%d')
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
    pass


def update_bars(
        date_to: str = datetime.now().strftime('%Y-%m-%d')
    ):
    """
    条件:
        何日地点までアップデートするかの日時。
    効果:
        データベースのbar情報を最新の状態に更新する。
    """
    rp = BarRepository(
        cli_db='DUMMY'
    ) # インポートテスト用
    pass