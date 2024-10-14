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


@decorator
def auto_insert(f, enable=False, *args, **kwargs):
    """
    ファクトリにより作成されたモデルをDBに自動で登録するデコレータ。
    ON,OFFを切り替え可能。
    """
    models: list[PeeweeTable] | PeeweeTable = f(*args, **kwargs)
    if not isinstance(models, list):
        models = [models]
    if enable:
        CLI_PEEWEE.insert_models(models)
    return models
