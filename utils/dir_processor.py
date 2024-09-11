# -*- CODING: UTF-8 -*-
# @time 2024/9/11 21:57
# @Author tyqqj
# @File dir_processor.py
# @
# @Aim
import os


# check if the directory exists
# if not, create it
def check_dir(dir_path: str) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Directory created: {dir_path}")
    else:
        # print(f"Directory already exists: {dir_path}")
        pass
    return None


# check if [base_dir, sub_dir, log_dir, model_dir] exist
# if not, create them
def check_dirs(args) -> None:
    check_list = ["base_dir", "sub_dir", "log_dir", "model_dir"]
    for item in check_list:
        if getattr(args, item) != 'None':
            check_dir(getattr(args, item))
        else:
            raise ValueError(f"Attribute {item} is None")
    return None
