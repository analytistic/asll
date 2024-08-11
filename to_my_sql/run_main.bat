@echo off
REM 设置工作目录
cd /d D:\asl\to_my_sql

REM 激活虚拟环境
call D:\asl\venv\Scripts\activate.bat

REM 运行 main.py
python main.py

REM 取消激活虚拟环境
deactivate
