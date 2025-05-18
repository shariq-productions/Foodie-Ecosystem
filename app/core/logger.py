import sys
from loguru import logger as _loguru_logger


class Log:
    def __init__(self):
        _loguru_logger.remove()

        _loguru_logger.add(
            sys.stdout,
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<green><level>{level: <8}</level></green> | "
                "\033[1m<cyan>{name}</cyan> : \033[1m<cyan>{function}</cyan> : \033[1m<cyan>at Line {line}</cyan>\033[0m  -  "
                "<level>{message}</level>"
            ),
            level="DEBUG",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        self._logger = _loguru_logger

    def info(self, message: str):
        self._logger.opt(depth=1).info(message)

    def debug(self, message: str):
        self._logger.opt(depth=1).debug(message)

    def warning(self, message: str):
        self._logger.opt(depth=1).warning(message)

    def error(self, message: str):
        self._logger.opt(depth=1).error(message)

    def critical(self, message: str):
        self._logger.opt(depth=1).critical(message)

    def success(self, message: str):
        self._logger.opt(depth=1).success(message)


# Exported instance
logger = Log()
