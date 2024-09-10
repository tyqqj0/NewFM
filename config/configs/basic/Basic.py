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

class Config(coqpit):
    seed: int = field(default=42, metadata={'help': 'seed'})
    log_dir: str = field(default='logs', metadata={'help': 'log directory'})
    model_dir: str = field(default='models', metadata={'help': 'model directory'})
    device : str = field(default='cuda', metadata={'help': 'device'})
    project : str = field(default='None', metadata={'help': 'project name'})
    run_name : str = field(default='None', metadata={'help': 'run name'})
    sub_dir : str = field(default='None', metadata={'help': 'sub directory in local directory: (log/model)/expeiements/runs'})
    use_wandb : bool = field(default=False, metadata={'help': 'use wandb for logging'})
    wandb_sweep : str = "???"