# -*- CODING: UTF-8 -*-
# @time 2024/9/10 21:03
# @Author tyqqj
# @File processor.py
# @
# @Aim


import importlib
import importlib.util
import os
from typing import List, Union, Dict, Any
from coqpit import Coqpit
from attr import dataclass

from ..paths import CONFIG_DIR, PROJECT_ROOT, UTILS_DIR


# TODO: 自动生成运行名称run_name，想想sweep的时候怎么处理
# sweep应该在sweep的时候处理，不应该在这里处理, run_name在basic.py处理好了
# 这个文件是用来处理config的继承关系解析的，将继承的config合并到一起


def load_Coqpit(config_path: str) -> Coqpit:
    """
    Load a Coqpit object from a config file.

    Args:
        config_path (str): The path to the config file.

    Returns:
        Coqpit: A Coqpit object representing the configuration.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
    """
    try:
        # try original path
        if not os.path.exists(config_path):
            raise FileNotFoundError
    except FileNotFoundError:
        if not os.path.exists(os.path.join(CONFIG_DIR, config_path)):
            raise FileNotFoundError
        else:
            config_path = os.path.join(CONFIG_DIR, config_path)

    # Load the config module
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    # Check for required attributes
    if not hasattr(config_module, 'Config'):
        raise AttributeError("Config file must contain 'Config' class")

    Config: Coqpit = config_module.Config

    # instantiate the config
    Config = Config.init_from_argparse()
    print(type(Config))
    Config.pprint()
    return Config


def load_configs_from_list(configs: List[str]) -> List[Coqpit]:
    """
    Load a list of Coqpit objects from a list of config files.

    Args:
        configs (List[str]): A list of paths to config files.

    Returns:
        List[Coqpit]: A list of Coqpit objects representing the configurations.

    Raises:
        FileNotFoundError: If any of the config files don't exist.
    """
    config_list = []
    for config_path in configs:
        config_list.append(load_Coqpit(config_path))
    return config_list


def process_config(config_path: str) -> Coqpit:
    """
        Process the config file, merging inherited configs into the main config.

        This function loads a config file, processes any inherited configs specified
        in the 'configs' list, and merges them into a single Coqpit object.

        Args:
            config_path (str): The path to the config file. Should contain a 'configs'
                               list and a 'Config' class.

        Returns:
            Coqpit: A Coqpit object representing the merged configuration.

        Raises:
            FileNotFoundError: If the config file doesn't exist.
            AttributeError: If the config file doesn't contain required attributes.

        Example:
            config = process_config("./config/configs/model/Resnet18.py")
            print(config.model_name)
            'Resnet18'
        """
    try:
        # try original path
        if not os.path.exists(config_path):
            raise FileNotFoundError
    except FileNotFoundError:
        if not os.path.exists(os.path.join(CONFIG_DIR, config_path)):
            raise FileNotFoundError

    # Load the config module
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    # Check for required attributes
    if not hasattr(config_module, 'configs') or not hasattr(config_module, 'Config'):
        raise AttributeError("Config file must contain 'configs' list and 'Config' class")

    configs: List[str] = config_module.configs
    Config: Coqpit = config_module.Config

    # first check if basic config is in the list, if not, add it
    if 'configs/basic/Basic.py' not in configs:
        configs.insert(0, 'configs/basic/Basic.py')

    # Process inherited configs
    # load configs as a list of Coqpit objects
    config_list = load_configs_from_list(configs)
    config_list.append(Config)
    # Merge the configs into the main config
    # Config should be last in the list
    main_config = config_list[0]
    print(type(main_config))
    main_config.pprint()
    for config in config_list[1:]:
        main_config = main_config.merge(config)

    return main_config
