# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:34
# @Author tyqqj
# @File Basic.py
# @
# @Aim 

import coqpit
from attr import dataclass, field

# Basic.py includes the basic arguments for the project, such as the seed, dirs.
# It includes the following arguments:
# seed: The seed for reproducibility
# log_dir: The directory where the logs will be saved
# model_dir: The directory where the models will be saved

class Basic(coqpit):
    seed: int = field(default=42, metadata={'help': 'seed'})
    log_dir: str = field(default='logs', metadata={'help': 'log directory'})
    model_dir: str = field(default='models', metadata={'help': 'model directory'})
