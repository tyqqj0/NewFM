# -*- CODING: UTF-8 -*-
# @time 2024/9/11 16:19
# @Author tyqqj
# @File __init__.py
# @
# @Aim 

from .paths import PROJECT_ROOT, UTILS_DIR, CONFIG_DIR
from .config_processor.processor import process_config
from .dir_processor import check_dirs
from .text import cprint, text_in_box, RichProgressIterator
import threading
from .log import get_logger

__all__ = ['PROJECT_ROOT', 'UTILS_DIR', 'CONFIG_DIR', 'process_config', 'check_dirs', 'cprint', 'text_in_box', 'RichProgressIterator']

_logger = None
_lock = threading.Lock()


def initialize_logger(config):
    global _logger
    with _lock:
        if _logger is None:
            _logger = get_logger(config)
    return _logger


class LoggerProxy:
    def __getattr__(self, name):
        global _logger, _lock
        if _logger is None:
            with _lock:
                if _logger is None:
                    raise RuntimeError("Logger未初始化。请先调用utils.initialize_logger(config)。")
        return getattr(_logger, name)

    def is_initialized(self):
        global _logger
        return _logger is not None


logger = LoggerProxy()
