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

from utils.arg import ConfigParser
from utils.text import text_in_box, RichProgressIterator

# import os
# import matplotlib.pyplot as plt
# import pandas as pd
# import torchvision

__all__ = ('BasicTask', 'BasicEpoch')


# TODO: 加保存


class BasicTask(ABC):
    config_json = './Basic.json'

    # current_file_path = os.path.abspath(__file__)
    # current_directory = os.path.dirname(current_file_path)
    # config_json = os.path.join(current_directory, 'Basic.json')

    # config = 0
    def __init__(self, config_dict=None, config_json=None, use_wandb=True, experiment_name='train', custom_run_name='',
                 api_key=None, group_name='basic'):
        self.custom_run_name = custom_run_name
        self.time = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        self.running = False
        self._run_name = None
        self.different_args = None
        if use_wandb:
            text_in_box('Use Wandb', color='red')
            print('Login Wandb...')
            wandb.login()
            print('Init Wandb...')
            wandb.init(project=experiment_name, name=self.run_name, group=group_name)
        self.api_key = api_key if api_key is not 'YOUR_API_KEY' else None
        text_in_box(f'Init Task run in {experiment_name}', color='orange')

        # self.config = ConfigParser(config_json or self.config_json).get_config()
        self.args = None
        self.use_wandb = use_wandb
        self.parse_args(config_json, config_dict)
        self.device = self.args.device
        self.experiment_name = experiment_name
        self.group_name = group_name
        # self.task = task

        #################DATA_params#################
        print('Building dataloader...')
        self.train_loader, self.val_loader = self.build_dataloader()
        # self.train_loader = track(self.train_loader, description='train')
        # self.val_loader = track(self.val_loader, description='val')
        #################Model_params#################
        print('Building model...')  #
        # self.model = None
        self.model = self.build_model().to(self.device)
        self.criterion = self.build_criterion()

        # self.run_name = ''

        #################Train_params#################
        print('Building Method...')
        # self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.epoch = 0
        self.max_epoch = self.args.max_epoch
        self.optimizer = self.build_optimizer()
        self.scheduler = self.build_scheduler()
        self.train_epoch = None
        self.val_epoch = None
        text_in_box(f'Init run {self.run_name} Done', color='orange')

    # def init(self):

    #################DATA_build#################
    @abstractmethod
    def build_dataloader(self):
        pass

    #################Model_build#################
    @abstractmethod
    def build_model(self):
        pass

    @abstractmethod
    def build_criterion(self):
        pass

    #################Train_build#################

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

    ##################internal#################

    # @classmethod
    def parse_args(self, config_json=None, config_dict=None):
        config = {}
        # for base_class in reversed(self.__class__.mro()):
        #     base_config_json = getattr(base_class, 'config_json', None)
        #     if base_config_json is not None:
        #         print(base_class)
        #         config = merge_configs(config, ConfigParser(base_config_json).get_config())
        # if config_json is not None:
        #     config = merge_configs(config, ConfigParser(config_json).get_config())
        # parser = ConfigParser(config_dict=config)
        # self.args = parser.parse_args()
        # self.different_args = parser.different
        # # if self.use_wandb:
        # #     wandb.config = self.config
        for base_class in reversed(self.__class__.mro()):
            base_config_json = getattr(base_class, 'config_json', None)
            if base_config_json is not None:
                print(f'Processing config for class: {base_class.__name__}')
                # 确保配置路径是正确的
                base_config_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), base_config_json)
                base_config_json = unify_slash(base_config_json)
                config = merge_configs(config, ConfigParser(base_config_json).get_config())

            # 如果提供了额外的配置路径
        if config_json is not None:
            config_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_json)
            config = merge_configs(config, ConfigParser(config_json).get_config())

        if config_dict is not None:
            if config_dict == 'agent' and self.use_wandb:
                config = merge_configs(config, wandb.config)
                self.different_args = merge_configs({}, wandb.config)
            elif isinstance(config_dict, dict):
                config = merge_configs(config, config_dict)
            elif config_dict == 'agent' and not self.use_wandb:
                pass
            else:
                raise ValueError(f'config_dict should be dict or "agent", now is {config_dict}')

            # 解析最终的配置字典
        parser = ConfigParser(config_dict=config)
        self.args = parser.parse_args()
        self.different_args = merge_configs(self.different_args, parser.different)

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

    def log_img(self, data, caption=None):
        # if self.use_wandb:
        #     wandb.log({caption: [wandb.Image(data)]}, step=self.epoch, commit=True)
        if isinstance(data, torch.Tensor):
            data = data.cpu().numpy()
        if self.use_wandb:
            wandb.log({caption: [wandb.Image(data)]}, step=self.epoch, commit=True)

    def log_tabel(self, data: list, columns=None, name='table'):
        if self.use_wandb:
            tabel = wandb.Table(columns=columns, data=data)
            wandb.log({name: tabel}, step=self.epoch, commit=True)

    # def

    # def _generate_run_name(self):
    #

    def run(self):
        text_in_box(f'Start Run {self.run_name}', color='magenta')
        if self.args is None:
            raise ValueError('Please use parse_args first')
        self.__property_check()
        if self.use_wandb:
            wandb.config.update(self.args)
        self.running = True
        self.run_train()
        # for epoch in range(1, self.max_epoch + 1):
        #     self.epoch = epoch
        #     self._run_epoch()
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
            raise ValueError(f"以下必要属性未设置或为None: {missing_str}")
        # print("所有必要属性已正确设置。")

    @property
    def run_name(self):
        if self.running:
            return self._run_name
        if self._run_name is None:
            # run_name
            optional_info = ''
            pass_arg = ['data_root']

            # self.run_name = self.experiment_name + '_' + self.group_name + '_'
            if self.different_args is not None:
                # 如果为空，不添加任何信息
                # print(self.different_args)
                if self.different_args is not {}:
                    for key, value in self.different_args.items():
                        if key in pass_arg:
                            continue
                        optional_info += f'{key}-{value}_'
            # self.run_name = self.run_name[:-1]
            # 如果运行已经开始，返回当前运行的 run_name

            # 每次调用 run_name 时，都会根据当前属性构造 run_name
            components = [
                self.custom_run_name,
                # self.args.model,
                # self.args.data_set,
                optional_info,
                self.time
            ]
            # 过滤掉空字符串，确保组件不为空
            valid_components = [component for component in components if component]
            # 使用下划线连接所有非空组件
            self._run_name = '_'.join(valid_components)
            return self._run_name
        else:
            return self._run_name

    @run_name.setter
    def run_name(self, value):
        # 如果需要，可以设置一个方法来允许外部修改 run_name 的一些组件
        # 这里的逻辑取决于您希望如何处理 run_name 的赋值
        pass


def merge_configs(parent_config: dict, child_config: dict):
    """合并两个配置字典，子配置覆盖父配置。"""
    if parent_config is None:
        parent_config = {}
    if child_config is None:
        child_config = {}
    if not isinstance(parent_config, dict) or not isinstance(child_config, dict):
        raise ValueError('Both parent_config and child_config should be dict')
    for key, value in child_config.items():
        if key in parent_config and isinstance(parent_config[key], dict) and isinstance(value, dict):
            merge_configs(parent_config[key], value)
        else:
            parent_config[key] = value
    return parent_config


# 统一路径中的斜杠
def unify_slash(path):
    return path.replace('\\', '/')


class BasicEpoch(ABC):
    def __init__(self, name, loader, task: BasicTask, color='white', bar=True):
        self.name = name
        self.epoch_count = 0
        self.task = task
        self.model = task.model
        self.criterion = task.criterion
        self.optimizer = task.optimizer
        self.scheduler = task.scheduler
        self.device = task.device
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

    # def print(self):
    #     if self.bar:
    def uprint(self, additional_info=""):
        if self.bar:
            # 假设 self.loader 是一个 tqdm 进度条对象
            self.loader.uprint(additional_info)
        else:
            print(additional_info)

    @abstractmethod
    def epoch(self):
        pass
