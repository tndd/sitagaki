from datetime import datetime

from loguru import logger


class LogClient:
    def __init__(self):
        self._configure_logger()

    def info(self, message: str, payload: dict | None = None):
        self._record_log("info", message, payload)

    def debug(self, message: str, payload: dict | None = None):
        self._record_log("debug", message, payload)

    def warn(self, message: str, payload: dict | None = None):
        self._record_log("warning", message, payload)

    def err(self, message: str, payload: dict | None = None):
        self._record_log("error", message, payload)

    def _configure_logger(self, log_path=None):
        """
        ログの形式と保存場所を設定
        """
        if log_path is None:
            log_path = f"log/data/{datetime.now().strftime('%Y/%m/%d/%H:%M:%S:%f')}.log"
        logger.add(
            log_path,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file.path} | {function} | {message} | {extra}",
            encoding='utf-8'
        )

    def _record_log(self, level: str, message: str, payload: dict | None):
        if payload is None:
            payload = {}
        log_method = getattr(logger, level)
        log_method(message, **payload)


CLI_LOG = LogClient()

# 使用例
CLI_LOG.info('これは情報メッセージです', {"user": "example_user", "action": "login"})
CLI_LOG.debug('これはデバッグメッセージです', {"user": "example_user", "action": "login"})
CLI_LOG.warn('これは警告メッセージです', {"user": "example_user", "action": "login"})
CLI_LOG.err('これはエラーメッセージです', {"user": "example_user", "action": "login"})
