# -*- CODING: UTF-8 -*-
# @time 2024/9/11 17:05
# @Author tyqqj
# @File template.py
# @
# @Aim 

from coqpit import Coqpit
from attr import dataclass, field

@dataclass
class Config(Coqpit):
    a: int = field(default=1, metadata={'help': 'a'})