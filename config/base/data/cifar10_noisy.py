# -*- coding: utf-8 -*-
"""
@File    :   cifar10_noisy.py
@Time    :   2024/10/12 23:38:29
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

from dataclasses import dataclass, field
import torch
from coqpit import Coqpit

# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np


@dataclass
class Config(Coqpit):
    max_data: int = field(default=10000, metadata={"help": "max number of data"})
    batch_size: int = field(default=64, metadata={"help": "batch size"})
    num_workers: int = field(default=0, metadata={"help": "number of workers"})
    pin_memory: bool = field(default=True, metadata={"help": "pin memory"})
    shuffle: bool = field(default=True, metadata={"help": "shuffle"})
    drop_last: bool = field(default=False, metadata={"help": "drop last"})
    download: bool = field(default=True, metadata={"help": "download"})
    data_path: str = field(default="/home/kevin/data", metadata={"help": "data path"})
    noise_type: str = field(default="symmetric", metadata={"help": "noise type"})
    noise_ratio: float = field(default=0.5, metadata={"help": "noise ratio"})
    seed: int = field(default=42, metadata={"help": "seed"})
