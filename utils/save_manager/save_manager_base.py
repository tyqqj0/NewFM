# -*- coding: utf-8 -*-
"""
@File    :   save_manager_base.py
@Time    :   2024/10/11 01:15:25
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

from abc import ABC, abstractmethod
import torch
import os
import sys
import time
import json

# import wandb
# import numpy as np


import numpy as np
import torch
from torch.utils import data
from torch import nn


class BaseSaveManager(ABC):
    @abstractmethod
    def log_metrics(self, data, step=None):
        pass

    @abstractmethod
    def log_plot(self, x, y, title=None, columns=None, name="plot", step=None):
        pass

    @abstractmethod
    def log_image(self, data, caption=None, step=None):
        pass

    @abstractmethod
    def log_table(self, data, columns=None, name="table", step=None):
        pass

    @abstractmethod
    def finalize(self):
        pass

    def _process_tensor(self, tensor) -> np.ndarray:
        """将PyTorch张量转换为NumPy数组"""
        return tensor.detach().cpu().numpy()

    def _process_dict(self, data) -> dict:
        """处理字典类型的数据,将PyTorch张量转换为NumPy数组"""
        # 如果不是字典，则返回原数据
        if not isinstance(data, dict):
            if isinstance(data, list) and len(data) == 2:
                data = {data[0]: data[1]}
            elif isinstance(data, tuple) and len(data) == 2:
                data = {data[0]: data[1]}
            else:
                raise ValueError("data should be dict or list or tuple")

        # 使用字典推导式进行优化
        processed_data = {
            key: (
                self._process_tensor(value)
                if isinstance(value, torch.Tensor)
                else value
            )
            for key, value in data.items()
        }
        return processed_data

    def _process_list(self, data) -> list:
        """处理列表类型的数据,将PyTorch张量转换为NumPy数组"""
        processed_data = [
            self._process_tensor(item) if isinstance(item, torch.Tensor) else item
            for item in data
        ]
        return processed_data
