@echo off

: check virtual environment
if not exist venv (
    python -m venv venv
)

set PYTHON="venv\Scripts\Python.exe"

: check pip packages
%PYTHON% -m pip install -r requirements.txt

: check directories
%PYTHON% .\utils\prepare.py

: have fun :)
%PYTHON% .\main.py

pause
