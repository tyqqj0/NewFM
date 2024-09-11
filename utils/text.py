# -*- CODING: UTF-8 -*-
# @time 2024/1/25 12:02
# @Author tyqqj
# @File text.py
# @
# @Aim 


def text_in_box(text, length=65, center=True, print_box=True, color='white'):
    # Split the text into lines that are at most `length` characters long
    lines = [text[i:i + length] for i in range(0, len(text), length)]

    # Create the box border, with a width of `length` characters
    up_border = '┏' + '━' * (length + 2) + '┓'
    down_border = '┗' + '━' * (length + 2) + '┛'
    # Create the box contents
    contents = '\n'.join(['┃ ' + (line.center(length) if center else line.ljust(length)) + ' ┃' for line in lines])

    # Combine the border and contents to create the final box
    box = '\n'.join([up_border, contents, down_border])

    if print_box:
        cprint(box, color)

    return box


COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m',
    'orange': '\033[38;5;208m',
    'gold': '\033[38;5;220m'
}

def cprint(text, color):
    if color not in COLORS:
        raise ValueError(f"不支持的颜色: {color}")
    print(f"{COLORS[color]}{text}{COLORS['reset']}")




# from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn
#
# class RichProgressIterator:
#     def __init__(self, iterable, description="Processing", total=None):
#         self.iterable = iterable
#         self.description = description
#         self.total = total if total is not None else len(iterable)
#         # 定义进度条样式
#         self.progress = Progress(
#             TextColumn("[bold cyan]{task.description}", justify="right"),
#             BarColumn(bar_width=None, complete_style="green", finished_style="bright_blue"),
#             TextColumn("[bold yellow]{task.completed} of {task.total}", justify="right"),
#             TextColumn("[bold magenta]{task.percentage:>3.0f}%", justify="right"),
#             TimeRemainingColumn(),
#             expand=True
#         )
#         self.task = None
#
#     def __iter__(self):
#         with self.progress:
#             self.task = self.progress.add_task(self.description, total=self.total)
#             for item in self.iterable:
#                 yield item
#                 self.progress.update(self.task, advance=1)
#
#     def update_description(self, new_description):
#         """ Update the progress bar description dynamically. """
#         if self.task is not None:
#             self.progress.update(self.task, description=new_description)


from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn

class RichProgressIterator:
    def __init__(self, iterable, description="Processing", total=None):
        self.iterable = iterable
        self.description = description
        self.total = total if total is not None else len(iterable)
        # 定义进度条样式
        self.progress = Progress(
            TextColumn("[bold cyan]{task.description}", justify="left"),
            BarColumn(bar_width=47, complete_style="green", finished_style="bright_blue"),
            TextColumn("[bold yellow]{task.completed} of {task.total}", justify="left"),
            TextColumn("[bold magenta]{task.percentage:>3.0f}%", justify="left"),
            TimeRemainingColumn(),
            expand=False
        )
        self.task = None

    def __iter__(self):
        with self.progress:
            self.task = self.progress.add_task(self.description, total=self.total)
            for item in self.iterable:
                yield item
                self.progress.update(self.task, advance=1)

    def uprint(self, new_description):
        """ Update the progress bar description dynamically. """
        if self.task is not None:
            self.progress.update(self.task, description=new_description)


# 分割线
def split_line(length=65):
    return '\n' + '━' * length + '\n'

