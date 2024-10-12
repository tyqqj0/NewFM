# -*- CODING: UTF-8 -*-
# @time 2024/9/11 14:52
# @Author tyqqj
# @File run.py
# @
# @Aim


import utils
from utils import logger, cprint, initialize_utils, save_manager
from coqpit import Coqpit
from trainers import get_trainer_class


def main(config_file: str, arg_dict: dict = None):
    # config = "config/users/Resnet18_CIFAR10_Supervised.py"
    args = utils.process_config(config_file)
    if arg_dict is not None:
        args.update(arg_dict)

    # args.pprint()

    # initialize utils
    initialize_utils(args)
    logger.info("Utils initialized")
    logger.info("Logger initialized")

    # run Trainer
    Trainer = get_trainer_class(args.trainer)
    if Trainer is None:
        logger.error(
            f"Trainer '{args.trainer}' not found. Please check config_file: {args.get_config_file_link()}"
        )
        return

    trainer = Trainer(args)
    trainer.train()

    return


if __name__ == "__main__":
    config = "users/Example.py"
    main(config)
# comparison = 1
