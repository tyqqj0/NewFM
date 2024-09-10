# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:19
# @Author tyqqj
# @File Resnet18_CIFAR10_Supervised.py
# @
# @Aim 


import coqpit
from attr import dataclass
from ..args.data import CIFAR10
from ..args.model import Resnet18
from ..args.training import Supervised


# import coqpit
# from attr import dataclass


# Define the configuration file for the ResNet18 model on CIFAR10 dataset
# The configuration file is a dictionary that contains the following keys:
# trainer.py: The file that contains the training script
# args.py: The file that contains the arguments for the training script
# use_wandb: A boolean that indicates whether to use Weights and Biases for logging
# device : The device to use for training, default is first available GPU
# project: The name of the project, whether to use Weights and Biases for logging
@dataclass
class Config(coqpit):
    trainer = "Resnet18_CIFAR_Supervised.py"
    arg = "Resnet18_CIFAR10_Supervised.py"
    use_wandb = True
    project = "Resnet18_CIFAR10_Supervised"
    device = "cuda:0"
