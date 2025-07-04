# -*- CODING: UTF-8 -*-
# @time 2024/6/6 下午7:52
# @Author tyqqj
# @File basic.py
# @
# @Aim
import time
from abc import ABC, abstractmethod

import torch

# from core.arg import ConfigParser
from utils import text_in_box
from core import logger, save_manager

# import os
# import matplotlib.pyplot as plt
# import pandas as pd
# import torchvision

__all__ = ("BasicTrainer", "BasicEpoch")


# TODO: 思考继承重复的问题
# TODO: 解决模块间通信问题
class BasicTrainer(ABC):

    def __init__(self, args):
        self.args = args
        logger.info("Trainer initializing")
        self.time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        self.running = False

        self.device = self._init_device()

        self._init_components()
        logger.info("Trainer initialized")
        text_in_box(f"Init run {self.args.run_name} Done", color="orange")

    def _init_device(self):
        if not torch.cuda.is_available():
            logger.warning("CUDA is not available, using CPU")
            return torch.device("cpu")

        if self.args.device.startswith("cuda"):
            try:
                device_index = (
                    int(self.args.device.split(":")[-1])
                    if ":" in self.args.device
                    else 0
                )
                device = torch.device(f"cuda:{device_index}")
                torch.cuda.set_device(device)
                logger.info(f"CUDA is available, using GPU {device_index}")
                return device
            except RuntimeError as e:
                logger.warning(f"Error setting CUDA device: {e}. Falling back to CPU.")
                return torch.device("cpu")
        else:
            logger.info("Device set to CPU in configuration")
            return torch.device("cpu")

    def _init_components(self):
        self.train_loader, self.val_loader, self.loaders = self.build_dataloader()
        # check loader, loaders should be dict or None
        if self.loaders is not None and not isinstance(self.loaders, dict):
            raise ValueError("loaders should be a dict or None")
        logger.info("Dataloader built")
        self.model = self.build_model().to(self.device)
        logger.info("Model built")
        self.criterion = self.build_criterion()
        logger.info("Criterion built")
        self.optimizer = self.build_optimizer()
        logger.info("Optimizer built")
        self.scheduler = self.build_scheduler()
        logger.info("Scheduler built")
        self.epochs = self.build_epochs()
        logger.info("Epochs built")
        self.epoch = 0
        self.max_epoch = self.args.max_epochs

    @abstractmethod
    def build_dataloader(self):
        pass

    @abstractmethod
    def build_model(self):
        pass

    @abstractmethod
    def build_criterion(self):
        pass

    @abstractmethod
    def build_optimizer(self):
        pass

    @abstractmethod
    def build_scheduler(self):
        pass

    @abstractmethod
    def build_epochs(self):
        pass

    @abstractmethod
    def run_epoch(self):
        pass

    def run_train(self):
        for epoch in range(1, self.max_epoch + 1):
            self.epoch = epoch
            text_in_box(f"Epoch {epoch}", color="white")
            logger.info(f"Epoch {epoch} start")
            log = self.run_epoch()
            save_manager.step = self.epoch + 1 # This will automatically commit the logs
            # save_manager.log_metrics(log, step=self.epoch)

    def run(self):
        text_in_box(
            f"Start Run train {self.args.run_name}, max_epoch: {self.max_epoch}",
            color="orange",
        )
        if self.args is None:
            raise ValueError("Please use parse_args first")
        self.__property_check()
        self.running = True
        self.run_train()
        self.running = False

    def __property_check(self):
        # 检查所有属性的设值情况
        required_properties = [
            "train_loader",
            "val_loader",
            "model",
            "criterion",
            "optimizer",
            "device",
            "epoch",
            "max_epoch",
            "running",
        ]
        missing_properties = [
            prop for prop in required_properties if getattr(self, prop, None) is None
        ]
        if missing_properties:
            missing_str = ", ".join(missing_properties)
            raise ValueError(f"Missing required properties: {missing_str}")
        # print("所有必要属性已正确设置。")


# def merge_configs(parent_config: dict, child_config: dict):
#     """合并两个配置字典，子配置覆盖父配置。"""
#     if parent_config is None:
#         parent_config = {}
#     if child_config is None:
#         child_config = {}
#     if not isinstance(parent_config, dict) or not isinstance(child_config, dict):
#         raise ValueError('Both parent_config and child_config should be dict')
#     for key, value in child_config.items():
#         if key in parent_config and isinstance(parent_config[key], dict) and isinstance(value, dict):
#             merge_configs(parent_config[key], value)
#         else:
#             parent_config[key] = value
#     return parent_config


# 统一路径中的斜杠
# def unify_slash(path):
#     return path.replace('\\', '/')
