from datetime import datetime

from loguru import logger

# JSON形式でログを保存するための設定
log_name = f"log/data/{datetime.now().strftime('%Y/%m/%d/%H:%M:%S:%f')}.log"
logger.add(log_name, serialize=True, encoding='utf-8')



def main_f():
    # 辞書型の情報を含むログメッセージの出力
    payload = {"user": "example_user", "action": "login"}
    logger.bind(**payload).debug('これはデバッグメッセージです')
    logger.bind(**payload).info('これは情報メッセージです')
    logger.bind(**payload).error('これはエラーメッセージです')

main_f()
