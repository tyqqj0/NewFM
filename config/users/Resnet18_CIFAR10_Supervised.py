# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:19
# @Author tyqqj
# @File Resnet18_CIFAR10_Supervised.py
# @
# @Aim 


import coqpit
from attr import dataclass
# from ..configs.basic import Basic
# from ..configs.data import CIFAR10
# from ..configs.model import Resnet18
# from ..configs.training import Supervised

configs = [
    "data/CIFAR10.py",
    "model/Resnet18.py",
    "training/Supervised.py"
]


# import coqpit
# from attr import dataclass


# Define the configuration file for the ResNet18 model on CIFAR10 dataset
# The configuration file is a dictionary that contains the following keys:
# trainer.py: The file that contains the training script
# configs.py: The file that contains the arguments for the training script
# use_wandb: A boolean that indicates whether to use Weights and Biases for logging
# device : The device to use for training, default is first available GPU
# project: The name of the project, whether to use Weights and Biases for logging
@dataclass
class Config(coqpit):
    trainer = "Resnet18_CIFAR_Supervised.py"
    project = "Resnet18_CIFAR10_Supervised"
    use_wandb = True

# # get() should be
# get() will not be use here, instead, the config will be automatically loaded from the config files when using run.py
# def get():
#     config = Basic.Config().init_from_argparse()
#     config.merge(CIFAR10.Config.init_from_argparse())
#     config.merge(Resnet18.Config.init_from_argparse())
#     config.merge(Supervised.Config.init_from_argparse())
#     config.merge(Config.init_from_argparse())
#     return config
