# -*- CODING: UTF-8 -*-
# @time 2024/9/10 20:19
# @Author tyqqj
# @File Resnet18.py
# @
# @Aim 

import coqpit
from attr import dataclass, field

class Config(coqpit):
    num_classes : int = field(default=10, metadata={'help': 'number of classes'})
    pretrained : bool = field(default=False, metadata={'help': 'pretrained'})
    num_channels : int = field(default=3, metadata={'help': 'number of channels'})
    fc : bool = field(default=True, metadata={'help': 'fc'})
    dropout : float = field(default=0.5, metadata={'help': 'dropout'})
    batch_norm : bool = field(default=True, metadata={'help': 'batch norm'})
