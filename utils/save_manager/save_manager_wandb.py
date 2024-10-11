# -*- coding: utf-8 -*-
"""
@File    :   save_manager_wandb.py
@Time    :   2024/10/11 01:15:32
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

# import wandb
# import numpy as np


import torch
import wandb
from .save_manager_base import BaseSaveManager

# utils/logger_wandb.py
import wandb
from .save_manager_base import BaseSaveManager


class WandbSaveManager(BaseSaveManager):
    def __init__(self, config):
        wandb.login()
        wandb.init(project=config.experiment_name, name=config.run_name)
        wandb.config.update(vars(config))
        self.use_wandb = True

    def log_metrics(self, data, step=None):
        wandb.log(data, step=step, commit=True)

    def log_plot(self, x, y, title=None, columns=None, name="plot", step=None):
        if columns is None:
            columns = ["x", "y"]
        data = list(zip(x, y))
        table = wandb.Table(columns=columns, data=data)
        wandb.log(
            {name: wandb.plot.line(table, columns[0], columns[1], title=title)},
            step=step,
            commit=True,
        )

    def log_image(self, data, caption=None, step=None):
        if isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        wandb.log({caption: [wandb.Image(data)]}, step=step, commit=True)

    def log_table(self, data, columns=None, name="table", step=None):
        table = wandb.Table(columns=columns, data=data)
        wandb.log({name: table}, step=step, commit=True)

    def finalize(self):
        wandb.finish()
