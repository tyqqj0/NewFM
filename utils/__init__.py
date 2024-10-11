# -*- CODING: UTF-8 -*-
# @time 2024/9/11 16:19
# @Author tyqqj
# @File __init__.py
# @
# @Aim

from .paths import PROJECT_ROOT, UTILS_DIR, CONFIG_DIR
from .config_processor.processor import process_config
from .dir_processor import process_dirs
from .text import cprint, text_in_box, RichProgressIterator
from .log import get_logger
from .save_manager import get_save_manager
from .metrics.average_meter import AverageMeter

__all__ = [
    "PROJECT_ROOT",
    "UTILS_DIR",
    "CONFIG_DIR",
    "process_config",
    "check_dirs",
    "cprint",
    "text_in_box",
    "RichProgressIterator",
    "initialize_utils",
    "AverageMeter",
]

_logger = None
_save_manager = None


def initialize_utils(args):
    global _logger, _save_manager

    # Process configuration
    config = process_config(args)

    # Check and create necessary directories
    process_dirs(config)

    # Initialize logger
    _logger = get_logger(config)

    # Initialize save manager
    _save_manager = get_save_manager(config)

    return config


class LoggerProxy:
    def __getattr__(self, name):
        global _logger, _lock
        if _logger is None:
            with _lock:
                if _logger is None:
                    raise RuntimeError(
                        "Logger is not initialized. Please call utils.initialize_utils(args) first."
                    )
        return getattr(_logger, name)

    def is_initialized(self):
        global _logger
        return _logger is not None


class SaveManagerProxy:
    def __getattr__(self, name):
        global _save_manager
        if _save_manager is None:
            raise RuntimeError(
                "SaveManager is not initialized. Please call utils.initialize_utils(args) first."
            )
        return getattr(_save_manager, name)


logger = LoggerProxy()
save_manager = SaveManagerProxy()
