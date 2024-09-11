# -*- CODING: UTF-8 -*-
# @time 2024/9/9 21:24
# @Author tyqqj
# @File arg.py
# @
# @Aim 


from coqpit import Coqpit

import inspect
from typing import Any, Type
from coqpit import Coqpit
from dataclasses import is_dataclass


def is_coqpit_subclass(config: Type[Any]) -> bool:
    """Check if the given class is a subclass of Coqpit."""
    return inspect.isclass(config) and issubclass(config, Coqpit)


def is_dataclass_check(config: Type[Any]) -> bool:
    """Check if the given class is a dataclass."""
    return is_dataclass(config)


def check_type_annotations(config: Type[Any]) -> list:
    """Check if all attributes have type annotations."""
    missing_annotations = []
    # 创建 __dict__ 的副本
    config_dict = dict(config.__dict__)
    for name, value in config_dict.items():
        if not name.startswith('__') and not callable(value):
            if name not in getattr(config, '__annotations__', {}):
                missing_annotations.append(name)
    return missing_annotations


def is_coqpit_instance(obj: Any) -> bool:
    """Check if the given object is an instance of a Coqpit subclass."""
    return isinstance(obj, Coqpit)


def is_empty_coqpit(instance: Coqpit) -> bool:
    """Check if the Coqpit instance is empty."""
    return not bool(vars(instance))


def check_common_attributes(instance: Coqpit) -> list:
    """Check for common configuration attributes."""
    common_attrs = ['seed', 'device', 'batch_size', 'learning_rate', 'num_epochs']
    missing_attrs = [attr for attr in common_attrs if not hasattr(instance, attr)]
    return missing_attrs


def check_callable_attributes(instance: Coqpit) -> list:
    """Check for any callable attributes."""
    return [name for name, value in vars(instance).items() if callable(value)]


def check_nested_coqpit(instance: Coqpit) -> list:
    """Check for nested Coqpit objects."""
    return [name for name, value in vars(instance).items() if isinstance(value, Coqpit)]


def config_check(config: Any):
    """
    Perform comprehensive checks on a config object or class.

    Args:
        config: The config object or class to check.
    """
    if inspect.isclass(config):
        print(f"Checking class: {config.__name__}")
        if not is_coqpit_subclass(config):
            print(f"Warning: {config.__name__} is not a subclass of Coqpit.")
        else:
            # print(f"{config.__name__} is a valid Coqpit subclass.")
            pass

        if not is_dataclass_check(config):
            print(f"Warning: {config.__name__} is not a dataclass. Consider using @dataclass decorator.")

        missing_annotations = check_type_annotations(config)
        if missing_annotations:
            print(f"Warning: The following attributes lack type annotations: {', '.join(missing_annotations)}")

        try:
            instance = config()
        except Exception as e:
            print(f"Error creating instance of {config.__name__}: {str(e)}")
            return
    else:
        if not is_coqpit_instance(config):
            print(f"Warning: The provided object is not an instance of a Coqpit subclass.")
            return
        instance = config
        # print(f"Checking instance of {type(instance).__name__}")

    if is_empty_coqpit(instance):
        print(f"Warning: The Coqpit instance is empty.")

    missing_common_attrs = check_common_attributes(instance)
    if missing_common_attrs:
        # print(f"Note: The following common attributes are missing: {', '.join(missing_common_attrs)}")
        pass

    callable_attrs = check_callable_attributes(instance)
    if callable_attrs:
        print(f"Warning: The following attributes are callable: {', '.join(callable_attrs)}")

    nested_coqpits = check_nested_coqpit(instance)
    if nested_coqpits:
        print(f"Note: Nested Coqpit objects found in attributes: {', '.join(nested_coqpits)}")

    # print("Config check completed.")


# Example usage:
if __name__ == "__main__":
    from dataclasses import dataclass


    @dataclass
    class SampleConfig(Coqpit):
        seed: int = 42
        device: str = "cuda"
        batch_size: int = 64

    # print()
    config_check(SampleConfig)
    config_check(SampleConfig())


    # Bad example
    class BadConfig:
        seed = 42
        device = "cuda"


    config_check(BadConfig)