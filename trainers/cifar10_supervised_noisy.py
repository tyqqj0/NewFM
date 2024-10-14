# -*- coding: utf-8 -*-
"""
@File    :   cifar10_supervised_noisy.py
@Time    :   2024/10/12 23:41:17
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch

# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np

import torch
from torch.utils.data import DataLoader

from components.epochs.visualization import Image2DEpoch
from components.epochs.supervised import TrainEpoch
from components.epochs.supervised import ValEpoch
from components.epochs.noisy import PseudoLabelTestEpoch
from components.models.classification.resnet18 import (
    ResNet18,
    get_criterion,
    get_optimizer,
    get_scheduler,
)
from components.data.classification import CIFAR10Dataset_Noisy, CIFAR10_transform
from trainers import BasicTrainer


# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np


class CIFAR10_noisy_Supervised(BasicTrainer):
    def __init__(self, args):
        super().__init__(args)

    def build_dataloader(self):
        train_transform = CIFAR10_transform(train=True)
        val_transform = CIFAR10_transform(train=False)

        train_dataset = CIFAR10Dataset_Noisy(
            root=self.args.data_path,
            train=True,
            transform=train_transform,
            download=self.args.download,
            noise_type=self.args.noise_type,
            noise_ratio=self.args.noise_ratio,
            seed=self.args.seed,
        )
        val_dataset = CIFAR10Dataset_Noisy(
            root=self.args.data_path,
            train=False,
            transform=val_transform,
            download=self.args.download,
            noise_type=None,
            noise_ratio=0,
            seed=self.args.seed,
        )

        train_loader = DataLoader(
            train_dataset, batch_size=self.args.batch_size, shuffle=True
        )
        val_loader = DataLoader(val_dataset, batch_size=self.args.batch_size)
        vis_loader = DataLoader(val_dataset, batch_size=1)

        return train_loader, val_loader, {"vis": vis_loader}

    def build_model(self):
        return ResNet18(num_classes=self.args.num_classes)

    def build_criterion(self):
        return get_criterion(self.args)

    def build_optimizer(self):
        return get_optimizer(self.args, self.model)

    def build_scheduler(self):
        if self.args.use_scheduler:
            return get_scheduler(self.args, self.optimizer)
        else:
            return None

    def build_epochs(self):
        train_epoch = TrainEpoch(
            name="train",
            loader=self.train_loader,
            trainer=self,
            color="blue",
            bar=True,
        )
        val_epoch = ValEpoch(
            name="val",
            loader=self.val_loader,
            trainer=self,
            color="green",
            bar=True,
        )
        pseudo_label_test_epoch = PseudoLabelTestEpoch(
            name="pseudo_label_test",
            loader=self.train_loader,
            trainer=self,
            color="red",
            bar=True,
        )

        epochs = {"train": train_epoch, "val": val_epoch, "pseudo_label_test": pseudo_label_test_epoch}
        return epochs

    def run_epoch(self):
        for phase in ["train", "val", "pseudo_label_test"]:
            self.epochs[phase].run()
