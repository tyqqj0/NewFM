#!/bin/bash

# 定义项目目录
# PROJECT_DIR="/home/kevin/code/NewFM"
PROJECT_DIR="."
# 显示目录绝对路径
echo "项目目录路径: $(pwd)"


# 导航到项目目录
cd $PROJECT_DIR || { echo "目录不存在: $PROJECT_DIR"; exit 1; }
# echo $PROJECT_DIR
# exit 1;

# 设置远程仓库 URL
REMOTE_URL="https://github.com/tyqqj0/NewFM.git"

    #  git config --global --add safe.directory /home/kevin/code/NewFM
# 添加到安全目录
git config --global --add safe.directory $PROJECT_DIR

# 确保远程仓库 URL 正确
git remote set-url origin $REMOTE_URL || { echo "设置远程仓库 URL 失败"; exit 1; }

# 拉取最新代码
echo "正在从 GitHub 拉取最新代码..."
git pull origin master || { echo "拉取失败"; exit 1; }

# 运行 Python 脚本
# echo "正在运行 Python 脚本..."
# python run.py || { echo "脚本运行失败"; exit 1; }

echo "操作完成！"