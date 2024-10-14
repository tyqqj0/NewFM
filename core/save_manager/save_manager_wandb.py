# -*- coding: utf-8 -*-
"""
@File    :   save_manager_wandb.py
@Time    :   2024/10/11 01:15:32
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import warnings
import numpy as np
import torch
import os
import sys
import time
import json

# import wandb
# import numpy as np


import torch

# import wandb
# from .save_manager_base import BaseSaveManager
from PIL import Image

# core/logger_wandb.py
import wandb
from .save_manager_base import BaseSaveManager


class WandbSaveManager(BaseSaveManager):
    def __init__(self, config):
        super().__init__()
        # 设置 wandb 的存储路径
        os.environ["WANDB_DIR"] = config.base_dir

        # 检查 wandb 是否已经初始化
        if wandb.run is None:
            # 如果未初始化，则进行初始化
            wandb.login()
            wandb.init(project=config.project_name, name=config.run_name)
            # 更新 wandb 的配置
            wandb.config.update(vars(config))
        else:
            # 如果已初始化，避免二次初始化，直接更新配置
            warnings.warn("wandb is already initialized, skip initialization")
            wandb.config.update(vars(config))

        self.use_wandb = True

    def commit(self):
        wandb.log({}, step=self.step, commit=True)

    def log_metrics(self, data, step):
        self.step = step
        # check if data is a dict
        if not isinstance(data, dict):
            raise ValueError(f"Data must be a dictionary, got {type(data)}")
        wandb.log(data, step=step, commit=False)

    def log_plot(self, x, y, step, title=None, columns=None, name="plot"):
        self.step = step

        if columns is None:
            columns = ["x", "y"]
        data = list(zip(x, y))
        table = wandb.Table(columns=columns, data=data)
        wandb.log(
            {name: wandb.plot.line(table, columns[0], columns[1], title=title)},
            step=step,
            commit=False,
        )

    def log_images(self, data, step, columns, name="images_table"):
        self.step = step
        # Check if the data format is correct
        if not all(isinstance(col, list) for col in data):
            raise ValueError(
                f"Incorrect data format. All columns should be lists. Found types: {[type(col) for col in data]}"
            )

        if any(len(col) != len(data[0]) for col in data):
            raise ValueError(
                f"Incorrect data format. All columns should have the same length. Number of columns: {len(data)}, Length of each column: {[len(col) for col in data]}"
            )

        # Check if the number of columns matches the number of data columns
        if len(columns) != len(data):
            raise ValueError(
                "The number of column names does not match the number of data columns."
            )

        # Convert data format
        table_data = list(zip(*data))

        # Process data based on its type
        for i, row in enumerate(table_data):
            table_data[i] = list(row)
            for j, item in enumerate(row):
                if isinstance(item, (torch.Tensor, np.ndarray, Image.Image)):
                    if isinstance(item, Image.Image):
                        pass
                    elif isinstance(item, (torch.Tensor, np.ndarray)):
                        image = self._process_tensor_auto(item)
                    if image is not None:
                        if isinstance(image, np.ndarray):
                                # print(image.shape)
                                # print(image)
                            table_data[i][j] = wandb.Image(image)
                        else:
                            table_data[i][j] = image
                elif isinstance(item, str):
                    table_data[i][j] = item
                elif isinstance(item, (int, float)):
                    table_data[i][j] = item
                else:
                    raise ValueError(f"Unsupported data type: {type(item)}")

        # Create wandb table
        table = wandb.Table(data=table_data, columns=columns)

        # Log the table
        wandb.log({name: table}, step=step, commit=False)

    def log_image(self, data, step, caption=None):
        self.step = step
        # PIL Image
        if isinstance(data, Image.Image):
            pass
        # torch Tensor
        elif isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        wandb.log({caption: [wandb.Image(data)]}, step=step, commit=False)

    def log_table(self, data, step, columns=None, name="table"):
        self.step = step
        table = wandb.Table(columns=columns, data=data)
        wandb.log({name: table}, step=step, commit=False)

    def finalize(self):
        wandb.finish()
