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
from typing import Optional
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
    def __init__(self):
        self.__step = 1

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Step must be an integer, got {type(value)}")
        if value is not None:
            if value == self.__step:
                return
            elif value > self.__step:
                print(f"Committing logs at step {self.__step}")
                self.commit()
                self.__step = value
            else:
                raise ValueError(f"Step must be equal or greater than current step {self.__step}, got {value}")

    @abstractmethod
    def commit(self):
        pass

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
    def log_images(self, data, caption=None, step=None):
        pass

    @abstractmethod
    def log_table(self, data, columns=None, name="table", step=None):
        pass

    @abstractmethod
    def finalize(self):
        pass

    def _process_tensor(self, tensor) -> np.ndarray:
        """将PyTorch张量转换为NumPy数组"""
        tensor = tensor.detach().cpu().numpy()
        # check type, convert to float if possible
        if tensor.dtype == np.float32:
            tensor = tensor.astype(np.float64)

        # if type is int, convert to float
        if tensor.dtype == np.int32:
            tensor = tensor.astype(np.float64)

        return tensor
    
    def _process_2d_tensor(self, tensor) -> np.ndarray:
        tensor = self._process_tensor(tensor)
        if tensor.ndim == 2:
            return tensor
        else:
            raise ValueError(f"Tensor must be 2D, got {tensor.ndim}D, {tensor.shape}")

    def _process_tensor_auto(self, tensor):
        tensor = self._process_tensor(tensor)
        if tensor.ndim == 4:
            if tensor.shape[0] == 1:
                tensor = tensor.squeeze(0)
            else:
                raise ValueError(f"Tensor must be 3D with shape (3, H, W), got {tensor.shape}")
        if tensor.ndim == 3:
            if tensor.shape[0] == 3 or tensor.shape[0] == 1:
                tensor = tensor.transpose(1, 2, 0)  # 将 (C, H, W) 转换为 (H, W, C)
            
            if tensor.shape[2] == 3 or tensor.shape[2] == 1:
                return tensor
            else:
                raise ValueError(f"Tensor must be 3D with shape (3, H, W) or (H, W, 1), got {tensor.shape}")
            # return tensor
        elif tensor.ndim == 2:
            return tensor
        elif tensor.ndim == 1:
            if tensor.shape[0] == 1:
                return tensor.squeeze(0).item()
            else:
                raise ValueError(f"Tensor 1D must be with shape (1,1), got {tensor.shape}")
        elif tensor.ndim == 0:
            return tensor.item()
        else:
            raise ValueError(f"Tensor must be 2D or 3D, got {tensor.ndim}D, {tensor.shape}")

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
