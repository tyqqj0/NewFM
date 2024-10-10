# -*- CODING: UTF-8 -*-
# @time 2024/6/6 下午7:52
# @Author tyqqj
# @File basic.py
# @
# @Aim
import os
import time
from abc import ABC, abstractmethod

import torch
import wandb
import coqpit

# from utils.arg import ConfigParser
from utils.text import text_in_box, RichProgressIterator

# import os
# import matplotlib.pyplot as plt
# import pandas as pd
# import torchvision

__all__ = ('BasicTrainer', 'BasicEpoch')


# TODO: 思考继承重复的问题
# TODO: 解决模块间通信问题
class BasicTrainer(ABC):

    def __init__(self, args):
        self.args = args
        self.time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        self.running = False
        self.use_wandb = args.use_wandb

        if self.args.use_wandb:
            self._init_wandb()

        self.device = torch.device(self.args.device)
        self._init_components()

    def _init_wandb(self):
        if not self.use_wandb:
            return
        text_in_box('Init Wandb', color='orange')
        wandb.login()
        wandb.init(project=self.args.experiment_name, name=self.args.run_name)
        wandb.config.update(self.args)

    def _init_components(self):
        print('Building dataloader...')
        self.train_loader, self.val_loader = self.build_dataloader()
        print('Building model...')  #
        self.model = self.build_model().to(self.device)
        print('Building trainer...')
        self.criterion = self.build_criterion()
        self.optimizer = self.build_optimizer()
        self.scheduler = self.build_scheduler()
        self.epoch = 0
        self.max_epoch = self.args.max_epoch
        text_in_box(f'Init run {self.args.run_name} Done', color='orange')

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
    def run_epoch(self):
        pass

    def run_train(self):
        for epoch in range(1, self.max_epoch + 1):
            self.epoch = epoch
            text_in_box(f'Epoch {epoch}', color='white')
            log = self.run_epoch()
            self.log_metrics(log)

    def log_metrics(self, data):
        if not isinstance(data, dict):
            if isinstance(data, list) and len(data) == 2:
                data = {data[0]: data[1]}
            elif isinstance(data, tuple) and len(data) == 2:
                data = {data[0]: data[1]}
            else:
                raise ValueError('data should be dict or list or tuple')
        if self.use_wandb:
            wandb.log(data, step=self.epoch, commit=True)
        print(data)

    def log_plot(self, x, y, title=None, columns=None, name='plot'):
        if columns is None:
            columns = ['x', 'y']
        data = list(zip(x, y))
        if self.use_wandb:
            tabel = wandb.Table(columns=columns, data=data)
            wandb.log({name: wandb.plot.line(tabel, columns[0], columns[1])}, step=self.epoch, commit=True, title=title)

    def log_img(self, data, caption=None):
        if isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        if self.use_wandb:
            wandb.log({caption: [wandb.Image(data)]}, step=self.epoch, commit=True)
        else:
            # 保存到本地
            pass

    def log_tabel(self, data: list, columns=None, name='table'):
        if self.use_wandb:
            tabel = wandb.Table(columns=columns, data=data)
            wandb.log({name: tabel}, step=self.epoch, commit=True)

    def run(self):
        text_in_box(f'Start Run train {self.args.run_name}', color='orange')
        if self.args is None:
            raise ValueError('Please use parse_args first')
        self.__property_check()
        if self.use_wandb:
            wandb.config.update(self.args)
        self.running = True
        self.run_train()

        self.running = False
        if self.use_wandb:
            wandb.finish()

    def __property_check(self):
        # 检查所有属性的设值情况
        required_properties = [
            'train_loader', 'val_loader', 'model', 'criterion', 'optimizer', 'device', 'epoch', 'max_epoch', 'running'
        ]
        missing_properties = [prop for prop in required_properties if getattr(self, prop, None) is None]
        if missing_properties:
            missing_str = ', '.join(missing_properties)
            raise ValueError(f"Missing required properties: {missing_str}")
        # print("所有必要属性已正确设置。")


class BasicEpoch(ABC):
    def __init__(self, name, loader, trainer: BasicTrainer, color='white', bar=True):
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
        self.loadert = loader
        self.loader = loader
        # 检查loader的返回值是否为三个，若不是则报错
        for a in loader:
            if len(a) != 3:
                print(a)
                raise ValueError(f'loader should return 3 values: inputs, targets, addition, got {len(a)}')
            else:
                break

    def run(self):
        self.epoch_count = self.epoch_count + 1
        text_in_box(f'{self.name} epoch {self.task.epoch}', color=self.color)
        if self.bar:
            self.loader = RichProgressIterator(self.loadert, description=f'{self.name} epoch')
        # print("start")
        return self.epoch()

    def uprint(self, additional_info=""):
        if self.bar:
            # 假设 self.loader 是一个 tqdm 进度条对象
            self.loader.uprint(additional_info)
        else:
            print(additional_info)

    @abstractmethod
    def epoch(self):
        pass

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
