from functools import wraps

from src.infra.db.peewee.client import CLI_PEEWEE, PeeweeTable


def auto_insert(func):
    """
    ファクトリに自動投入関数を付与するデコレータ。
    FUCTORY_FUNC.load()と呼び出すことで、DBへのインサートが可能。

    NOTE:
        少しでも込み入ったことをするとなると、
        pip-decoratorは使い物にならないので、
        このデコレータは直書きしてる。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        基本的にはファクトリ関数をそのまま返す
        だからauto_insertデコレータをつけるだけでなら無害だ。
        """
        return func(*args, **kwargs)

    def load(*args, **kwargs):
        """
        .load()が呼び出された場合、DBへのインサートが行われる。
        """
        result: list[PeeweeTable] | PeeweeTable = func(*args, **kwargs)
        # ファクトリの戻り値はリストだけでなく単体の可能性もあるため、リストに変換
        models = [result] if not isinstance(result, list) else result
        CLI_PEEWEE.insert_models(models)
        return result

    wrapper.load = load
    return wrapper
