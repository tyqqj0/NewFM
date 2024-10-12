# -*- coding: utf-8 -*-
"""
@File    :   logger_local.py
@Time    :   2024/10/11 01:01:14
@Author  :   Author
@Version :   1.0
@Contact :   Contact
@Desc    :   None
"""

import torch
import os
import sys
import time
import json
import csv
import matplotlib.pyplot as plt
import pandas as pd

# import wandb
# import numpy as np


# utils/logger_local.py
from .save_manager_base import BaseSaveManager


class LocalSaveManager(BaseSaveManager):
    def __init__(self, config):
        self.log_dir = config.log_dir
        self.run_name = config.run_name
        self.log_file = open(
            os.path.join(self.log_dir, f"{self.run_name}_log.txt"), "a"
        )
        self.metrics_file = open(
            os.path.join(self.log_dir, f"{self.run_name}_metrics.csv"), "a"
        )
        self.metrics_writer = csv.writer(self.metrics_file)
        self.metrics_writer.writerow(["step", "metric", "value"])  # 写入CSV文件的表头
        self.use_wandb = False

    def log_metrics(self, data, step=None):
        data = self._process_dict(data)
        self.log_file.write(f"Step {step}: {data}\n")

        for metric, value in data.items():
            self.metrics_writer.writerow([step, metric, value])

            metric_file = open(
                os.path.join(self.log_dir, f"{self.run_name}_{metric}.md"), "a"
            )
            metric_file.write(f"## Step {step}\n")
            metric_file.write(f"- {metric}: {value}\n\n")
            metric_file.close()

    def log_plot(self, x, y, title=None, columns=None, name="plot", step=None):
        if columns is None:
            columns = ["x", "y"]

        data = pd.DataFrame({columns[0]: x, columns[1]: y})
        data.to_csv(
            os.path.join(self.log_dir, f"{self.run_name}_{name}_{step}.csv"),
            index=False,
        )

        plt.figure()
        plt.plot(x, y)
        if title:
            plt.title(title)
        plt.xlabel(columns[0])
        plt.ylabel(columns[1])
        plt.savefig(os.path.join(self.log_dir, f"{self.run_name}_{name}_{step}.png"))
        plt.close()

    def log_image(self, data, caption=None, step=None):
        if isinstance(data, torch.Tensor):
            data = self._process_tensor(data)

        plt.figure()
        plt.imshow(data)
        if caption:
            plt.title(caption)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(self.log_dir, f"{self.run_name}_image_{step}.png"))
        plt.close()

    def log_images(self, data, caption=None, step=None):
        for i, image in enumerate(data):
            self.log_image(image, caption=caption[i] if caption else None, step=step)

    def log_table(self, data, columns=None, name="table", step=None):
        data = self._process_dict(data)

        if columns is None:
            columns = list(data.keys())

        table_data = [[col] + [data[col]] for col in columns]
        table = pd.DataFrame(table_data, columns=["Metric", "Value"])

        table_file = os.path.join(self.log_dir, f"{self.run_name}_{name}_{step}.md")
        with open(table_file, "w") as f:
            f.write(table.to_markdown(index=False))

    def finalize(self):
        self.log_file.close()
        self.metrics_file.close()
