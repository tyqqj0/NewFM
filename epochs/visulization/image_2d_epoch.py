# -*- coding: utf-8 -*-
"""
@File    :   image_2d.py
@Time    :   2024/10/11 23:50:14
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


from epochs.basic_epoch import BasicEpoch
from utils import logger, save_manager


class Image2DEpoch(BasicEpoch):
    def __init__(self, name, loader, trainer, color=None, bar=None, max_samples=10):
        super().__init__(
            name=name, loader=loader, trainer=trainer, color=color, bar=bar
        )
        self.max_samples = max_samples

    def epoch(self):
        self.model.eval()

        results = [[], [], []]
        for _ in range(self.max_samples):
            inputs, targets, _ = next(iter(self.loader))
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)

            output = self.model(inputs)
            preds = output.argmax(dim=1)

            results[0].append(inputs)
            results[1].append(targets)
            results[2].append(preds)

        return results

    def after_epoch(self, result: dict):
        save_manager.log_images(result, ["inputs", "targets", "preds"])
