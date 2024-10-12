# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:34
# @Author tyqqj
# @File Basic.py
# @
# @Aim
import datetime
import os
from dataclasses import asdict, dataclass, field
from typing import Any

import utils

from coqpit import Coqpit

# from attr import
from coqpit import check_argument


# Basic.py includes the basic arguments for the project, such as the seed, dirs.
# It includes the following arguments:
# seed: The seed for reproducibility
# log_dir: The directory where the logs will be saved
# model_dir: The directory where the models will be saved


@dataclass
class Config(Coqpit):
    trainer: str = field(default="None", metadata={"help": "trainer file"})
    seed: int = field(default=42, metadata={"help": "seed"})
    # log_dir: base_dir + 'logs'
    device: str = field(default="cuda", metadata={"help": "device"})
    project_name: str = field(default="Default", metadata={"help": "project name"})
    run_name: str = field(default="None", metadata={"help": "run name"})
    base_dir: str = field(default="runs", metadata={"help": "base directory"})
    use_wandb: bool = field(default=False, metadata={"help": "use wandb for logging"})

    sub_dir: str = field(default="None")
    log_dir: str = field(default="None")
    model_dir: str = field(default="None")

    config_file_path: str = field(default="", metadata={"help": "配置文件的路径"})

    def __post_init__(self):
        super().__post_init__()
        self._update_dirs()

    def _update_dirs(self) -> None:
        if self.base_dir == "None":
            self.base_dir = os.path.join(utils.PROJECT_ROOT, "runs")
        if not os.path.isabs(self.base_dir):
            self.base_dir = os.path.join(utils.PROJECT_ROOT, self.base_dir)

        if self.run_name == "None":
            self.run_name = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

        self.sub_dir = os.path.join(self.base_dir, self.project_name, self.run_name)
        self.log_dir = os.path.join(self.sub_dir, "logs")
        self.model_dir = os.path.join(self.sub_dir, "models")

    # wandb_sweep : str = "???" # sweep shouldn't be here

    def check_values(
        self,
    ):
        # print("here")
        self._update_dirs()
        # print(self)
        ca = asdict(self)
        # print(ca)
        # ca = self.to_dict()
        # print(ca)
        check_argument("seed", ca, restricted=True)
        check_argument("device", ca, restricted=True, allow_none=False)
        check_argument("project_name", ca, restricted=True, allow_none=False)
        check_argument("run_name", ca, restricted=True, allow_none=False)
        check_argument("base_dir", ca, restricted=True, allow_none=False)
        # check_argument("sub_dir", ca, restricted=True, allow_none=False)
        # check_argument("log_dir", ca, restricted=True, allow_none=False)
        # check_argument("model_dir", ca, restricted=True, allow_none=False)

        return self

    # def is_parsed(self):
    #     self._is_parsed = True

    def get_config_file_link(self) -> str:
        if not self.config_file_path:
            return "配置文件路径未设置"
        
        abs_config_path = os.path.abspath(self.config_file_path)
        return f"\033]8;;file://{abs_config_path}\033\\{abs_config_path}\033]8;;\033\\"

    def set_config_file_path(self, path: str):
        self.config_file_path = path

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name in ["project_name", "run_name", "base_dir"]:
            self.check_values()

    def __getattr__(self, item):
        if item in ["project_name", "run_name", "base_dir"]:
            self._update_dirs()
        return super().__getattribute__(item)


if __name__ == "__main__":
    # c = Config()
    # # print("before parse", c.keys())
    # c.parse_args()
    # # print("after parse", c.keys())
    # print(c.pprint())
    pass
