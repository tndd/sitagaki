from pydantic import BaseModel


class BarRepository(BaseModel):
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
        戻り値:
            DFもしくはエラー
        効果:
            対象期間のローソク足をDB上から取得し保存する。
        """
        # TODO
        pass