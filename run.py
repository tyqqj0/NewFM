# -*- CODING: UTF-8 -*-
# @time 2024/9/11 14:52
# @Author tyqqj
# @File run.py
# @
# @Aim


import core
from core import logger, initialize_utils, save_manager
from utils import cprint, text_in_box
from coqpit import Coqpit
from trainers import get_trainer_class


def main(config_file: str, arg_dict: dict = None):
    # config = "config/experiments/resnet18_cifar10_supervised.py"
    args = core.process_config(config_file)
    if arg_dict is not None:
        args.update(arg_dict)

    text_in_box(f"Config:", color="orange")
    args.pprint()

    # initialize core
    initialize_utils(args)
    logger.info("Utils initialized")
    logger.info("Logger initialized")

    # run Trainer
    Trainer = get_trainer_class(args.trainer)
    if Trainer is None:
        logger.error(
            f"Trainer '{args.trainer}' not found. Please check config_file: {args.get_config_file_link()}"
        )
        return>

    trainer = Trainer(args)
    trainer.run()

    return


if __name__ == "__main__":
    config = "experiments/resnet18_cifar10_supervised.py"
    # parse config file path
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=config)
    args, unknown = parser.parse_known_args()

    print("config:", args.config)
    main(args.config)
    # comparison = 1
