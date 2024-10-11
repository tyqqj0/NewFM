# -*- coding: utf-8 -*-
"""
@File    :   save_manager_wandb.py
@Time    :   2024/10/11 01:15:32
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import numpy as np
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

        # TODO: 设置wandb的存储路径，已完成
        os.environ["WANDB_DIR"] = config.base_dir
        wandb.login()
        wandb.init(project=config.project_name, name=config.run_name)
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

    def log_images(self, data, columns, name="images_table", step=None):
        # Check if the data format is correct
        if not all(isinstance(col, list) for col in data) or any(
            len(col) != len(data[0]) for col in data
        ):
            raise ValueError(
                "Incorrect data format. Please ensure all columns are lists and have the same length."
            )

        # Check if the number of columns matches the number of data columns
        if len(columns) != len(data):
            raise ValueError(
                "The number of column names does not match the number of data columns."
            )

        # Convert data format
        table_data = list(zip(*data))

        # Process image data
        for i, row in enumerate(table_data):
            table_data[i] = list(row)
            for j, item in enumerate(row):
                if isinstance(item, (str, torch.Tensor, np.ndarray)):
                    table_data[i][j] = wandb.Image(item)

        # Create wandb table
        table = wandb.Table(data=table_data, columns=columns)

        # Log the table
        wandb.log({name: table}, step=step, commit=True)

    def log_image(self, data, caption=None, step=None):
        if isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        wandb.log({caption: [wandb.Image(data)]}, step=step, commit=True)

    def log_table(self, data, columns=None, name="table", step=None):
        table = wandb.Table(columns=columns, data=data)
        wandb.log({name: table}, step=step, commit=True)

    def finalize(self):
        wandb.finish()
