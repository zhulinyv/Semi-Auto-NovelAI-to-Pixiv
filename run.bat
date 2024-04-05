@echo off

: check virtual environment
if not exist venv (
    python -m venv venv
)

: start g4f
.\g4f.vbs

set PYTHON="venv\Scripts\Python.exe"

: check pip packages
%PYTHON% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

: check directories
%PYTHON% .\utils\predir.py

: have fun :)
%PYTHON% .\main.py

pause