# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:19
# @Author tyqqj
# @File Resnet18_CIFAR10_Supervised.py
# @
# @Aim


from coqpit import Coqpit

# from attr import dataclass
from dataclasses import asdict, dataclass, field

# from ..configs.basic import Basic
# from ..configs.data import CIFAR10
# from ..configs.model import Resnet18
# from ..configs.training import Supervised

configs = [
    "configs/data/CIFAR10.py",
    "configs/model/Resnet18.py",
    "configs/training/Supervised.py",
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
    trainer: str = "CIFAR10_Supervised.py"
    project_name: str = "Resnet18_CIFAR10_Supervised"
    use_wandb: bool = True


if __name__ == "__main__":
    print(Config())
