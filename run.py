# -*- CODING: UTF-8 -*-
# @time 2024/9/11 14:52
# @Author tyqqj
# @File run.py
# @
# @Aim


import utils
from utils import logger, cprint, initialize_utils, save_manager, text_in_box
from coqpit import Coqpit
from trainers import get_trainer_class


def main(config_file: str, arg_dict: dict = None):
    # config = "config/users/Resnet18_CIFAR10_Supervised.py"
    args = utils.process_config(config_file)
    if arg_dict is not None:
        args.update(arg_dict)


    text_in_box(f"Config:", color="orange")
    args.pprint()

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
    trainer.run()

    return


if __name__ == "__main__":
    config = "users/Resnet18_CIFAR10_Supervised.py"
    main(config)
    # comparison = 1
