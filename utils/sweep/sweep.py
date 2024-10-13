# -*- coding: utf-8 -*-
"""
@File    :   sweep.py
@Time    :   2024/10/12 22:33:49
@Author  :   tyqqj
@Version :   1.0
@Contact :   tyqqj0@163.com
@Desc    :   wandb sweep
"""

import wandb
import yaml
import os
import sys

# 添加项目根目录到 Python 路径
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_dir)

import run  # 导入 run.py 模块


def main():
    # wandb 会自动初始化，无需显式调用 wandb.init()
    # 从 wandb.config 获取参数
    config_dict = dict(wandb.config)
    # 调用 run.py 中的 main 函数
    run.main("experiments/resnet18_cifar10_supervised.py", config_dict)


def create_sweep(file):
    # 读取 sweep 配置
    with open(file, "r") as f:
        sweep_config = yaml.safe_load(f)
    print(sweep_config)
    # 创建 sweep
    sweep_id = wandb.sweep(sweep_config)
    return sweep_id


if __name__ == "__main__":
    import argparse

    # parse file path or sweep_id
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=str, default="tyqqj_ai/Resnet18_CIFAR10_Supervised/kts6y3zm"
    )
    args, _ = parser.parse_known_args()

    file = args.file

    # if is a path then load, if is sweep_id then use it
    if os.path.exists(file):
        sweep_id = create_sweep(file)
    else:
        sweep_id = file

    # 高亮显示
    print(f"\033[92m{sweep_id}\033[0m")

    # 启动 wandb agent
    wandb.agent(sweep_id, function=main)
