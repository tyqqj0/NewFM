# -*- CODING: UTF-8 -*-
# @time 2024/9/11 14:52
# @Author tyqqj
# @File run.py
# @
# @Aim


import utils
from utils import logger, cprint, initialize_utils, save_manager
from coqpit import Coqpit


def main(config: str, arg_dict: dict = None):
    # config = "config/users/Resnet18_CIFAR10_Supervised.py"
    args = utils.process_config(config)
    if arg_dict is not None:
        args.update(arg_dict)

    # process dirs
    utils.process_dirs(args)
    cprint("Configuration file processed successfully", "green")

    # print args
    args.pprint()

    # initialize utils
    utils.initialize_utils(args)
    logger.info("Utils initialized")
    logger.info("Logger initialized")
    cprint("Utils initialized", "green")
    cprint("Logger initialized", "green")

    # run Trainer
    # TODO: Trainer
    return None


if __name__ == "__main__":
    config = "users/Example.py"
    main(config)
# comparison = 1
