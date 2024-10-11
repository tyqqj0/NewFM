# -*- coding: utf-8 -*-
"""
@File    :   __init__.py
@Time    :   2024/10/11 01:15:14
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch
import os
import sys
import time
import json
#import wandb
#import numpy as np


# utils/logger_factory.py
from .save_manager_wandb import WandbSaveManager
from .save_manager_local import LocalSaveManager

def get_save_manager(config):
    #TODO: 这个部分逻辑需要重新想
    # 这块先这样写，后面加上了其他save_manager再改，要加选项冲突检查
    if config.use_wandb:
        return WandbSaveManager(config)
    else:
        return LocalSaveManager(config)
