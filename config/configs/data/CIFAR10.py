# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:19
# @Author tyqqj
# @File CIFAR10.py
# @
# @Aim 


from coqpit import Coqpit
from attr import dataclass, field

@dataclass
class Config(Coqpit):
    max_data : int = field(default=10000, metadata={'help': 'max number of data'})
    batch_size : int = field(default=64, metadata={'help': 'batch size'})
    num_workers : int = field(default=0, metadata={'help': 'number of workers'})
    pin_memory : bool = field(default=True, metadata={'help': 'pin memory'})
    shuffle : bool = field(default=True, metadata={'help': 'shuffle'})
    drop_last : bool = field(default=False, metadata={'help': 'drop last'})
    download : bool = field(default=False, metadata={'help': 'download'})
