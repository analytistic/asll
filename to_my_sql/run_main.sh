#!/bin/bash
# 设置工作目录
cd /path_to/asl/to_my_sql || exit

# 激活虚拟环境
source /path_to/venv/bin/activate

# 运行 main.py
python main.py

# 取消激活虚拟环境
deactivate
