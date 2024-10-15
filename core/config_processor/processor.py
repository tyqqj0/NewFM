# -*- CODING: UTF-8 -*-
# @time 2024/9/10 21:03
# @Author tyqqj
# @File processor.py
# @
# @Aim


import importlib
import importlib.util
import os
from typing import List, Union, Dict, Any, Type
from coqpit import Coqpit
import abc
from pprint import pprint
import dataclasses

# from attr import dataclass

from ..paths import CONFIG_DIR, PROJECT_ROOT, CORE_DIR


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
    # Check if the file exists
    if not os.path.exists(config_path):
        alternative_path = os.path.join(CONFIG_DIR, config_path)
        if os.path.exists(alternative_path):
            config_path = alternative_path
        else:
            raise FileNotFoundError(f"Config file not found: {config_path}")

    # Load the config module
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    # Check for required attributes
    if not hasattr(config_module, "Config"):
        raise AttributeError("Config file must contain 'Config' class")

    ConfigClass = config_module.Config  # Coqpit class

    # print(f"ConfigClass: {ConfigClass}")
    # print(f"Is subclass of Coqpit: {issubclass(ConfigClass, Coqpit)}")

    # # 尝试查看 Config 类的属性
    # print("Config class attributes:")
    # for attr in dir(ConfigClass):
    #     if not attr.startswith("__"):
    #         print(f"  {attr}: {getattr(ConfigClass, attr)}")

    # 实例化配置
    try:
        # config_instance = ConfigClass.init_from_argparse(arg_prefix='')
        config_instance = ConfigClass
        # print(f"Config instance type: {type(config_instance)}")
        # print("Config instance attributes:")
        # for attr in dir(config_instance):
        #     if not attr.startswith("__"):
        #         print(f"  {attr}: {getattr(config_instance, attr)}")

        # 尝试使用 to_dict() 方法
        if hasattr(config_instance, "to_dict"):
            # print("Config as dict:")
            # print(config_instance.to_dict())
            pass
        else:
            # print("to_dict() method not found")
            pass

        # 尝试使用 pprint() 方法
        if hasattr(config_instance, "pprint"):
            # print("Config pprint:")
            # config_instance.pprint()
            pass
        else:
            # print("pprint() method not found")
            pass

    except Exception as e:
        print(f"Error instantiating Config: {e}")
        raise

    # check if config_instance is a subclass of Coqpit
    if not isinstance(config_instance, type) or not issubclass(config_instance, Coqpit):
        raise TypeError(
            f"Config instance must be a subclass of Coqpit, but got {type(config_instance)}"
        )

    return config_instance


def load_config_class(config_path: str) -> Type[Coqpit]:
    # Adjust config_path if necessary
    if not os.path.isabs(config_path):
        config_path = os.path.join(CONFIG_DIR, config_path)

    # Load the config module
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    # Check if Config class exists
    if not hasattr(config_module, "Config"):
        raise AttributeError(f"Config file must contain 'Config' class: {config_path}")

    return config_module.Config


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
    Process the config file, merging inherited base into the main config.

    This function loads a config file, processes any inherited base specified
    in the 'base' list, and merges them into a single Coqpit object.

    Args:
        config_path (str): The path to the config file. Should contain a 'base' list and a 'Config' class.

    Returns:
        Coqpit: A Coqpit object representing the merged configuration.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        AttributeError: If the config file doesn't contain required attributes.

    Example:
        config = process_config("./config/base/model/resnet18.py")
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
        else:
            config_path = os.path.join(CONFIG_DIR, config_path)

    # Load the config module
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    # Check if the module was imported successfully
    if not config_module:
        raise ImportError(f"Failed to import the config module from {config_path}")

    # Check for required attributes
    if not hasattr(config_module, "configs") or not hasattr(config_module, "Config"):
        raise AttributeError(
            "Config file must contain 'configs' list and 'Config' class"
        )

    configs: List[str] = config_module.configs  # str list
    Config: Coqpit = config_module.Config  # Coqpit class

    # Config = Config()  # Coqpit instance

    # first check if basic config is in the list, if not, add it
    if "base/basic/Basic.py" not in configs:
        configs.insert(0, "base/basic/Basic.py")
    # print("configs:")
    # for config in configs:
    #     print(config)
    if 0:
        print("config_list:")
        for config in config_list:
            print(config)
    # Process inherited base
    # load base as a list of Coqpit objects
    config_list = []
    for config_path in configs:
        config_list.append(load_config_class(config_path))
    config_list.append(Config)
    # important: base config should be the first one in the list

    MergedConfig = merge_config_classes(config_list)  #
    # MergedConfig = Config

    # 显示 Config 类的所有方法
    # print(f"Config class methods: {dir(Config)}")
    # pprint(dataclasses.fields(MergedConfig))

    # instantiate the Config class
    config_instance = MergedConfig.init_from_argparse(arg_prefix="")

    # set config_file_path
    config_instance.set_config_file_path(config_path)

    # if main_config have a _update_dirs method, call it
    if hasattr(config_instance, "check_values"):
        config_instance.check_values()

    return config_instance


def merge_config_classes(config_classes: List[Type[Coqpit]]) -> Type[Coqpit]:
    """
    merge config classes into one class
    use multi-inheritance to merge config classes
    important: class order in the list is the order of inheritance
    """
    import dataclasses
    from dataclasses import MISSING, field, make_dataclass

    # 收集所有字段的信息
    field_dict = {}
    for cls in config_classes:
        for f in dataclasses.fields(cls):
            field_dict[f.name] = f  # 后面的字段会覆盖前面的同名字段

    fields = []
    for field_name, field_obj in field_dict.items():
        field_type = field_obj.type
        field_params = {}
        if field_obj.default is not MISSING:
            field_params["default"] = field_obj.default
        elif field_obj.default_factory is not MISSING:
            field_params["default_factory"] = field_obj.default_factory
        field_params["metadata"] = field_obj.metadata
        new_field = field(**field_params)
        fields.append((field_name, field_type, new_field))

    # 创建合并后的数据类，继承所有配置类
    MergedConfig = make_dataclass(
        cls_name="MergedConfig",
        fields=fields,
        bases=tuple(config_classes),  # 让 MergedConfig 继承所有配置类
    )

    # print("MergedConfig has fields:")
    # for field in dataclasses.fields(MergedConfig):
    #     print(f"- {field.name}: {field.type}")

    return MergedConfig
