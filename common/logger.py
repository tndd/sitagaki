from datetime import datetime

from loguru import logger

from common.workmode import CURRENT_WORK_MODE, only_test

# ログの吐き先はワークモードによって変わる
_log_dir = CURRENT_WORK_MODE.value.lower()
_log_path = f"log/{_log_dir}/{datetime.now().strftime('%Y/%m/%d')}.log"


def get_logger(path: str = _log_path):
    """
    ワークモードごとにログは独立している。
    ログディレクトリは'年/月/日付.log'という単位で更新される形式。

    NOTE: get_loggerの利用について
        この関数は原則として外部からは呼ばれない。
        ログ機能を利用する際には下部に定義されているLOGをインポートする。

        ただしテストなどでログを部分的に複製したいという特別な用途において、
        この関数が利用されることはあり得る。
    """
    logger.add(
        path,
        format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {file.path} | {function} | {message} | {extra}",
        encoding='utf-8'
    )
    return logger


def build_payload(
    conditon: dict | None = None,
    exception: Exception | None = None,
    extra: dict | None = None,
):
    """
    payloadに例外オブジェクトの情報を追加して返す

    condition:
        引数など、これを呼び出した関数の実行状態を再現するための情報
    exception:
        例外オブジェクトなど、エラーについての詳細な情報
    extra:
        いずれにも当てはまらないが、必要な追記事項
    """
    payload = {}
    if conditon:
        payload['__COND__'] = conditon
    if exception:
        payload['__EXCP__'] = exception.args
    if extra:
        payload['__EXTRA__'] = extra
    return payload


def read_log():
    """
    現在の吐き先ログファイルの全体を読み込む
    """
    with open(_log_path, 'r') as f:
        return f.readlines()


def read_log_latest_line():
    """
    吐き先ログファイルの直近一行を読み込む
    """
    lines = read_log()
    return lines[-1]


@only_test
def clear_log():
    """
    ログをクリアする。
    危険な関数なのでテスト環境以外では実行できないようにしておく。
    """
    with open(_log_path, 'w') as f:
        f.truncate(0)


# 基本的には、このLOGをインポートする形でログ機能を利用する。
LOG = get_logger()