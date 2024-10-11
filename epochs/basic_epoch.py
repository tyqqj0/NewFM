# -*- coding: utf-8 -*-
"""
@File    :   basic_epoch.py
@Time    :   2024/10/11 19:00:06
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""


from abc import ABC, abstractmethod

import torch

from utils.text import RichProgressIterator, text_in_box
from utils import logger


# import wandb
# import numpy as np


class BasicEpoch(ABC):
    def __init__(self, name, loader, trainer, color="white", bar=True):
        self.name = name
        self.epoch_count = 0
        self.task = trainer
        self.model = trainer.model
        self.criterion = trainer.criterion
        self.optimizer = trainer.optimizer
        self.scheduler = trainer.scheduler
        self.device = trainer.device
        self.color = color
        self.bar = bar
        self.__check_loader(loader)
        self.loader_oringinal = loader
        self.loader = loader

    def run(self):
        self.epoch_count = self.epoch_count + 1
        text_in_box(f"{self.name} epoch {self.task.epoch}", color=self.color)
        logger.info(f"{self.name} epoch {self.task.epoch} start")
        if self.bar:
            self.loader = RichProgressIterator(
                self.loader_oringinal, description=f"{self.name} epoch"
            )
        self.before_epoch()
        result = self.epoch()
        # check the result
        if result is not None and not isinstance(result, dict):
            logger.error(f"{self.name} epoch return value must be a dict")
            raise ValueError(f"{self.name} epoch return value must be a dict")
        self.after_epoch(result)
        if self.bar:
            self.loader.close()
        logger.info(f"{self.name} epoch {self.task.epoch} end")
        return result

    def uprint(self, additional_info=""):
        if self.bar:
            # 假设 self.loader 是一个 tqdm 进度条对象
            self.loader.uprint(additional_info)
        else:
            logger.info(additional_info)
            # print(additional_info)

    def before_epoch(self):
        return None

    @abstractmethod
    def epoch(self) -> dict:
        pass

    def after_epoch(self, result: dict):
        # suggest to log the result in here
        logger.warning(
            f"after_epoch has not been implemented in {self.name}, suggest to log the result in here"
        )
        return None

    def __check_loader(self, loader):
        if loader is None:
            logger.error("Loader not properly set")
            raise ValueError("Loader not properly set")
        try:
            sample = next(iter(loader))
        except Exception as e:
            logger.error(f"Loader not working properly: {e}")
            raise ValueError(f"Loader not working properly: {e}")

        if len(sample) != 3:
            logger.error(
                f"Loader should return 3 values: inputs, targets, addition, but returned {len(sample)} values"
            )
            raise ValueError(
                f"Loader should return 3 values: inputs, targets, addition, but returned {len(sample)} values"
            )

        inputs, targets, addition = sample
        if not isinstance(inputs, torch.Tensor) or not isinstance(
            targets, torch.Tensor
        ):
            logger.error("Loader should return inputs and targets as tensor types")
            raise ValueError("Loader should return inputs and targets as tensor types")

        if not isinstance(addition, dict) or "index" not in addition:
            logger.error(
                "Loader should return addition as a dictionary containing at least an 'index' key"
            )
            raise ValueError(
                "Loader should return addition as a dictionary containing at least an 'index' key"
            )
