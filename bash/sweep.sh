#!/bin/bash

# 运行 pull.sh 并确保路径正确
# bash "$(dirname "$0")/pull.sh", $0 是当前脚本的文件名
cd "$(dirname "$0")"
# echo "当前目录: $(pwd)"

# 检查是否有正在运行的 sweep.py 的 tmux 会话
sessions=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | grep sweep_py_session)

if [ -n "$sessions" ]; then
    echo "检测到以下正在运行的 sweep.py 会话："
    select session in $sessions "启动新的会话"; do
        if [ "$session" == "启动新的会话" ]; then
            break
        elif [ -n "$session" ]; then
            echo "正在连接到会话 $session..."
            tmux attach-session -t $session
            exit 0
        else
            echo "无效选择，请重新选择。"
        fi
    done
fi


cd ../
echo "进入工作目录: $(pwd)"


# 启动新的 tmux 会话运行 sweep.py, 并确保路径正确
session_name="sweep_py_$(date +%Y%m%d_%H%M%S)"
echo "启动新的 tmux 会话：$session_name"
tmux new-session -s $session_name -d "python ./utils/sweep/sweep.py"

# 连接到新启动的会话
tmux attach-session -t $session_name
