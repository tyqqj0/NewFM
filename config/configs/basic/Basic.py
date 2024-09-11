# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:34
# @Author tyqqj
# @File Basic.py
# @
# @Aim
import datetime
import os
from dataclasses import asdict, dataclass, field
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
    trainer: str = field(default='None', metadata={'help': 'trainer file'})
    seed: int = field(default=42, metadata={'help': 'seed'})
    # log_dir: base_dir + 'logs'
    device: str = field(default='cuda', metadata={'help': 'device'})
    project_name: str = field(default='Default', metadata={'help': 'project name'})
    run_name: str = field(default='None', metadata={'help': 'run name'})
    base_dir: str = field(default='runs', metadata={'help': 'base directory'})
    sub_dir: str = field(default='None', metadata={'help': 'sub directory in local directory: \\base_dir\\project\\run_name'})
    log_dir: str = field(default='None', metadata={'help': 'log directory: \\base_dir\\project\\run_name\\logs'})
    model_dir: str = field(default='None', metadata={'help': 'model directory: \\base_dir\\project\\run_name\\models'})
    use_wandb: bool = field(default=False, metadata={'help': 'use wandb for logging'})

    # wandb_sweep : str = "???" # sweep shouldn't be here

    def check_values(self, ):
        # print("here")
        # if self.use_wandb:
        # process base_dir, if base_dir is not absolute path, then make it absolute path
        if self.base_dir == 'None':
            self.base_dir = os.path.join(utils.PROJECT_ROOT, 'runs')
        if self.base_dir != 'None' and not os.path.isabs(self.base_dir):
            self.base_dir = os.path.join(utils.PROJECT_ROOT, self.base_dir)
        # setting the default value for run_name and sub_dir
        if self.run_name == 'None':
            # using time as the default run_name
            self.run_name = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        if self.sub_dir == 'None':
            # using project name as the default sub_dir
            self.sub_dir = os.path.join(self.base_dir, self.project_name, self.run_name)
        if self.log_dir == 'None':
            self.log_dir = os.path.join(self.sub_dir, 'logs')
        if self.model_dir == 'None':
            self.model_dir = os.path.join(self.sub_dir, 'models')
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
        check_argument("sub_dir", ca, restricted=True, allow_none=False)
        check_argument("log_dir", ca, restricted=True, allow_none=False)
        check_argument("model_dir", ca, restricted=True, allow_none=False)

        return self


if __name__ == '__main__':
    c = Config()
    # print("before parse", c.keys())
    c.parse_args()
    # print("after parse", c.keys())
    print(c.pprint())
