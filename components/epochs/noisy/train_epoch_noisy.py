# -*- coding: utf-8 -*-
"""
@File    :   train_epoch_noisy.py
@Time    :   2024/10/12 23:48:31
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   Test Pesudo-labeling accuracy
"""

# import torch


import torch

from components.epochs.basic_epoch import BasicEpoch
from core import logger, save_manager
from utils import AverageMeter

# import os
# import sys
# import time
# import json
# import wandb
# import numpy as np


def diffculty(output, mode="entropy", normalize=True):
    """
    Compute confidence score for each sample based on the predicted probabilities.

    Args:
        pred_probs (numpy.ndarray): Predicted probability matrix with shape (n_samples, n_classes).
        mode (str): Confidence score computation mode. Options: 'max_prob', 'entropy', 'margin'.

    Returns:
        confidence_scores (numpy.ndarray): Confidence score array with shape (n_samples,).
    """

    output = torch.nan_to_num(output)

    output = torch.clamp(output, 0, 1)
    if normalize:
        # nom = torch.sum(output, dim=1)
        # nom = nom + 1e-7
        # output = output / nom.unsqueeze(1)
        # softmax
        output = torch.softmax(output, dim=1)  # 可以对函数值加限制

    # print(output)

    assert output.ndim == 2, "Input must be a 2D probability matrix."

    if mode == "max_prob":
        confidence_scores = -torch.max(output, axis=1)[0]
    elif mode == "entropy":
        confidence_scores = -torch.sum(output * torch.log(output + 1e-7), axis=1)
        # print(confidence_scores)
        # confidence_scores = 1 - confidence_scores / torch.log(torch.tensor(output.shape[1]))
    elif mode == "margin":
        # sorted_probs = torch.sort(output, axis=1)[:, ::-1]
        # confidence_scores = (sorted_probs[:, 0] - sorted_probs[:, 1]) / 2 + 0.5

        sorted_probs, _ = torch.sort(
            output, dim=1, descending=True
        )  # 使用dim而不是axis，并且添加descending=True直接得到逆序
        confidence_scores = -((sorted_probs[:, 0] - sorted_probs[:, 1]) / 2 + 0.5)
        print(confidence_scores)
        if not torch.isfinite(confidence_scores).all():
            print("Non-finite values detected")

            # 可以选择将这些值设置为0或其他有意义的数字
            confidence_scores[~torch.isfinite(confidence_scores)] = 0
    else:
        raise ValueError("Unsupported confidence score mode.")

    if normalize:
        print(confidence_scores.min(), confidence_scores.max())
        # confidence_scores = (confidence_scores - confidence_scores.min()) / (
        #         confidence_scores.max() - confidence_scores.min())
        min_val = confidence_scores.min()
        max_val = confidence_scores.max()

        if max_val == min_val:
            print("All confidence scores are the same.")
            print(confidence_scores.min(), confidence_scores.max())
            confidence_scores = torch.zeros_like(
                confidence_scores
            )  # 所有值都设置为0或其他处理方式
        else:
            confidence_scores = (confidence_scores - min_val) / (max_val - min_val)

    # print(output[torch.argmax(confidence_scores)], confidence_scores[torch.argmax(confidence_scores)])

    return confidence_scores


class PesudoLabelTestEpoch(BasicEpoch):
    def __init__(self, name, loader, trainer, color="blue", bar=True):
        super().__init__(
            name=name, loader=loader, trainer=trainer, color=color, bar=bar
        )

    def epoch(self):
        self.model.eval()

        # iterate the loader
        for inputs, targets, addition in self.loader:
            inputs, targets = inputs.to(self.device), targets.to(self.device)

            # forward
            outputs, _ = self.model(inputs)
            
            diffculty_scores = diffculty(outputs)
            
            self.plot_histogram([proba, truett], epoch, folder='prob', pre='prob') if self.plot_histogram else None

            # gmm find the noisy samples

        return

    def after_epoch(self, result: dict):
        print(f"Epoch {self.epoch_count} result: {result}")
        save_manager.log_metrics(result, step=self.epoch_count)
