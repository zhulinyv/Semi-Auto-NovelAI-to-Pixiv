@echo off

: check virtual environment
if not exist venv (
    python -m venv venv
)

set PYTHON="venv\Scripts\Python.exe"

: check pip packages
%PYTHON% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

: have fun :)
%PYTHON% .\main.py

pause