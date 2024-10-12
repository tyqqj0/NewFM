# -*- coding: utf-8 -*-
"""
@File    :   CIFAR10_Supervised.py
@Time    :   2024/10/12 00:28:32
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   None
"""

import torch
from torch.utils.data import DataLoader

from epochs.visulization import Image2DEpoch
from epochs.supervised import TrainEpoch
from epochs.supervised import ValEpoch
from models.classicification.resnet18 import (
    resnet18,
    get_criterion,
    get_optimizer,
    get_scheduler,
)
from data.classicification import CIFAR10Dataset, CIFAR10_transform
from trainers import BasicTrainer


# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np


class CIFAR10_Supervised(BasicTrainer):
    def __init__(self, args):
        super().__init__(args)

    def build_dataloader(self):
        train_transform = CIFAR10_transform(train=True)
        val_transform = CIFAR10_transform(train=False)

        train_dataset = CIFAR10Dataset(
            root=self.args.data_path,
            train=True,
            transform=train_transform,
            download=self.args.download,
        )
        val_dataset = CIFAR10Dataset(
            root=self.args.data_path,
            train=False,
            transform=val_transform,
            download=self.args.download,
        )

        train_loader = DataLoader(
            train_dataset, batch_size=self.args.batch_size, shuffle=True
        )
        val_loader = DataLoader(val_dataset, batch_size=self.args.batch_size)
        vis_loader = DataLoader(val_dataset, batch_size=1)

        return train_loader, val_loader, {"vis": vis_loader}

    def build_model(self):
        return resnet18(num_classes=self.args.num_classes)

    def build_criterion(self):
        return get_criterion(self.args)

    def build_optimizer(self):
        return get_optimizer(self.args, self.model)

    def build_scheduler(self):
        return get_scheduler(self.args, self.optimizer)

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
        image_2d_epoch = Image2DEpoch(
            name="image_2d",
            loader=self.loaders["vis"],
            trainer=self,
            color="red",
            bar=False,
            max_samples=3,
        )

        epochs = {"train": train_epoch, "val": val_epoch, "image_2d": image_2d_epoch}
        return epochs

    def run_epoch(self):
        for phase in ["train", "val", "image_2d"]:
            self.epochs[phase].run()
