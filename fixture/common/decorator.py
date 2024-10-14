from functools import wraps

from decorator import decorator

from src.infra.db.common import is_test_mode
from src.infra.db.peewee.client import CLI_PEEWEE


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
        models = func(*args, **kwargs)
        if not isinstance(models, list):
            models = [models]
        if INSERT:
            CLI_PEEWEE.insert_models(models)
        return models
    return wrapper
