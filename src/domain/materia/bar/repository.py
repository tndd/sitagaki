from dataclasses import dataclass


@dataclass
class BarRepository:
    def fetch_bars(symbol: str, start: str, end: str):
        """
        条件:
            シンボルと開始日、終日を指定。
        効果:
            対象期間のローソク足をDBから取得し保存する。
            もしもDBにデータが存在しなければ、オンライン上からの取得を試みる。
        """
        # IMPL
        pass


    ### PRIVATE
    def pull_bars_from_online(symbol: str, start: str, end: str):
        """
        条件:
            シンボルと開始日、終日を指定。
        効果:
            対象期間のローソク足をオンライン上から取得し保存する。
        """
        # IMPL
        pass


    def fetch_bars_from_local(symbol: str, start: str, end: str):
        """
        条件:
            シンボルと開始日、終日を指定。
        効果:
            対象期間のローソク足をDB上から取得し保存する。
        """
        # TODO
        pass