from functools import wraps

from decorator import decorator

from src.infra.db.common import is_test_mode
from src.infra.db.peewee.client import CLI_PEEWEE, PeeweeTable


@decorator
def only_test(f, *args, **kwargs):
    """
    テストモード以外で実行するとエラーを吐き強制終了させるデコレータ。
    """
    if not is_test_mode():
        raise ValueError("テストモードではないため、実行できません。 EID:019d3665")
    return f(*args, **kwargs)


def auto_insert(func):
    """
    ファクトリにより作成されたモデルをDBに自動で登録するデコレータ。
    INSERTを指定することでON,OFFを切り替え可能。
    デフォルトではOFF。

    少しでも込み入ったことをするとなると、pip-decoratorは使い物にならない。
    """
    @wraps(func)
    def wrapper(*args, INSERT=False, **kwargs):
        result: list[PeeweeTable] | PeeweeTable = func(*args, **kwargs)
        if INSERT:
            # 単体のテーブルモデルを返すファクトリもあるので、その場合はリストに変換
            models = [result] if not isinstance(result, list) else result
            CLI_PEEWEE.insert_models(models)
        return result
    return wrapper
