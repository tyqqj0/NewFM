# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:34
# @Author tyqqj
# @File Basic.py
# @
# @Aim
import datetime
from dataclasses import asdict

from coqpit import Coqpit
from attr import dataclass, field
from coqpit import check_argument


# Basic.py includes the basic arguments for the project, such as the seed, dirs.
# It includes the following arguments:
# seed: The seed for reproducibility
# log_dir: The directory where the logs will be saved
# model_dir: The directory where the models will be saved

@dataclass
class Config(Coqpit):
    seed: int = field(default=42, metadata={'help': 'seed'})

    # log_dir: base_dir + 'logs'
    device: str = field(default='cuda', metadata={'help': 'device'})
    project_name: str = field(default='Default', metadata={'help': 'project name'})
    run_name: str = field(default='None', metadata={'help': 'run name'})
    base_dir: str = field(default='runs', metadata={'help': 'base directory'})
    sub_dir: str = field(default='None', metadata={'help': 'sub directory in local directory: /base_dir/project/run_name'})
    log_dir: str = field(default='None', metadata={'help': 'log directory: /base_dir/project/run_name/logs'})
    model_dir: str = field(default='None', metadata={'help': 'model directory: /base_dir/project/run_name/models'})
    use_wandb: bool = field(default=False, metadata={'help': 'use wandb for logging'})

    # wandb_sweep : str = "???" # sweep shouldn't be here

    def check_values(self):

        # if self.use_wandb:
        # setting the default value for run_name and sub_dir
        if self.run_name == 'None':
            # using time as the default run_name
            self.run_name = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        if self.sub_dir == 'None':
            # using project name as the default sub_dir
            self.sub_dir = self.base_dir + '/' + self.project_name + '/' + self.run_name
        if self.log_dir == 'None':
            self.log_dir = self.sub_dir + '/logs'
        if self.model_dir == 'None':
            self.model_dir = self.sub_dir + '/models'
        c = asdict(self)
        check_argument("seed", c["seed"], restricted=True)
        check_argument("device", c["device"], restricted=True, allow_none=False)
        check_argument("project_name", c["project_name"], restricted=True, allow_none=False)
        check_argument("run_name", c["run_name"], restricted=True, allow_none=False)
        check_argument("base_dir", c["base_dir"], restricted=True, allow_none=False)
        check_argument("sub_dir", c["sub_dir"], restricted=True, allow_none=False)
        check_argument("log_dir", c["log_dir"], restricted=True, allow_none=False)
        check_argument("model_dir", c["model_dir"], restricted=True, allow_none=False)

        return self
