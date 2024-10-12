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

        results = [[], [], [], []]
        for i, (inputs, targets, _) in enumerate(self.loader):
            if i >= self.max_samples:
                break
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)

            output = self.model(inputs)
            preds = output.argmax(dim=1)

            # shape from (1, C, H, W) to (H, W, C)
            results[0].append(self.epoch_count)
            results[1].append(inputs.cpu().squeeze(0).permute(1, 2, 0))
            results[2].append(targets.cpu().squeeze(0))
            results[3].append(preds.cpu().squeeze(0))
            

        return {"results": results}

    def after_epoch(self, result: dict):
        save_manager.log_images(
            data=result["results"], columns=["epoch", "inputs", "targets", "preds"], name=self.name, step=self.epoch_count
        )
