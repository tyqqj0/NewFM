# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:18
# @Author tyqqj
# @File Supervised.py.py
# @
# @Aim 


from coqpit import Coqpit
# from attr import dataclass, field
from dataclasses import asdict, dataclass, field

@dataclass
class Config(Coqpit):
    max_epochs : int = field(default=100, metadata={'help': 'max number of epochs'})
    lr : float = field(default=0.1, metadata={'help': 'learning rate'})
    momentum : float = field(default=0.9, metadata={'help': 'momentum'})
    weight_decay : float = field(default=5e-4, metadata={'help': 'weight decay'})
    log_interval : int = field(default=10, metadata={'help': 'log interval, including visualization'})
    save_interval : int = field(default=100, metadata={'help': 'save interval'})
    resume : str = field(default=None, metadata={'help': 'resume'})
