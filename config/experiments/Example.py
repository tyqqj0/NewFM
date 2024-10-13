# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:19
# @Author tyqqj
# @File resnet18_cifar10_supervised.py
# @
# @Aim


from coqpit import Coqpit

# from attr import dataclass
from dataclasses import asdict, dataclass, field

# from ..base.basic import Basic
# from ..base.data import CIFAR10
# from ..base.model import Resnet18
# from ..base.training import Supervised

configs = [
    "base/data/cifar10.py",
    "base/model/resnet18.py",
    "base/training/supervised.py",
]


# import coqpit
# from attr import dataclass


# Define the configuration file for the ResNet18 model on CIFAR10 dataset
# The configuration file is a dictionary that contains the following keys:
# trainer.py: The file that contains the training script
# use_wandb: A boolean that indicates whether to use Weights and Biases for logging
# project: The name of the project, whether to use Weights and Biases for logging
@dataclass
class Config(Coqpit):
    trainer: str = "CIFAR10_Supervised"
    project_name: str = "Example"
    use_wandb: bool = False


if __name__ == "__main__":
    print(Config())
