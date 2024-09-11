# -*- CODING: UTF-8 -*-
# @time 2024/9/11 14:52
# @Author tyqqj
# @File run.py
# @
# @Aim 


import utils
from utils import logger
from coqpit import Coqpit


def main(config: str, arg_dict: dict = None):
    # config = "config/users/Resnet18_CIFAR10_Supervised.py"
    args = utils.process_config(config)
    if arg_dict is not None:
        args.update(arg_dict)
    utils.check_dirs(args)
    utils.cprint("Configuration file processed successfully", "green")
    args.pprint()
    utils.initialize_logger(args)
    logger.info("Logger initialized")
    utils.cprint("Logger initialized", "green")

    # run Trainer
    # TODO: Trainer
    return None


if __name__ == '__main__':
    config = "config/users/Resnet18_CIFAR10_Supervised.py"
    main(config)
# comparison = 1
