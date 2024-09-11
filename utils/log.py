# -*- CODING: UTF-8 -*-
# @time 2024/9/11 22:40
# @Author tyqqj
# @File log.py
# @
# @Aim

import logging
import os
from typing import Optional
import colorlog

def setup_logger(name: str, log_dir: str, level: int = logging.INFO) -> logging.Logger:
    """
        设置一个日志记录器，可以同时输出到控制台（彩色）和文件。

        Args:
            name (str): 日志记录器的名称
            log_dir (str): 日志文件保存的目录
            level (int): 日志级别，默认为 INFO

        Returns:
            logging.Logger: 配置好的日志记录器
        """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 创建控制台处理器（彩色）
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(level)

    # 创建文件处理器
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(os.path.join(log_dir, f"{name}.log"))
    file_handler.setLevel(level)

    # 创建彩色格式化器（用于控制台）
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    console_handler.setFormatter(color_formatter)

    # 创建普通格式化器（用于文件）
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 使用示例
def get_logger(config: Optional[object] = None) -> logging.Logger:
    """
    获取或创建一个全局日志记录器。

    Args:a
        config (object, optional): 配置对象，包含 log_dir 属性

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    if not hasattr(get_logger, "logger"):
        log_dir = config.log_dir if config and hasattr(config, 'log_dir') else 'logs'
        # print()
        get_logger.logger = setup_logger("project_name", log_dir)
    return get_logger.logger

# 使用示例
if __name__ == "__main__":
    # logger = get_logger()
    # logger.info("这是一条信息日志")
    # logger.warning("这是一条警告日志")
    # logger.error("这是一条错误日志")
    logger = get_logger()
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")