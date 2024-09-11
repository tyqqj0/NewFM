# -*- CODING: UTF-8 -*-
# @time 2024/9/11 14:52
# @Author tyqqj
# @File run.py
# @
# @Aim 



import utils
from coqpit import Coqpit

if __name__ == '__main__':
    config = "config/users/Resnet18_CIFAR10_Supervised.py"
    args = utils.process_config(config)
    # print(args)
    print(type(args))
    print(issubclass(type(args), Coqpit))
    args.pprint()