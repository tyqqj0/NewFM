# -*- CODING: UTF-8 -*-
# @time 2024/9/11 16:19
# @Author tyqqj
# @File __init__.py
# @
# @Aim 

from .paths import PROJECT_ROOT, UTILS_DIR, CONFIG_DIR
from .config_processor.processor import process_config
from .dir_processor import check_dirs
from .text import cprint, text_in_box, RichProgressIterator



