from datetime import datetime

from loguru import logger


class LogClient:
    def __init__(
        self,
        log_path: str = f"log/data/{datetime.now().strftime('%Y/%m/%d')}.log"
    ):
        # ログの保存先は外部からも確認できるようにしておく
        self.log_path = log_path
        self.setup_logger()

    def info(self, message: str, payload: dict | None = None):
        self._record_log("info", message, payload)

    def debug(self, message: str, payload: dict | None = None):
        self._record_log("debug", message, payload)

    def warn(self, message: str, payload: dict | None = None):
        self._record_log("warning", message, payload)

    def error(self, message: str, payload: dict | None = None):
        self._record_log("error", message, payload)

    def setup_logger(self):
        """
        ログの形式と保存場所を設定
        """
        logger.add(
            self.log_path,
            format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {file.path} | {function} | {message} | {extra}",
            encoding='utf-8'
        )

    def _record_log(self, level: str, message: str, payload: dict | None):
        if payload is None:
            payload = {}
        log_method = getattr(logger, level)
        log_method(message, **payload)


CLI_LOG = LogClient()
