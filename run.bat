@echo off

: check virtual environment
if not exist venv (
    python -m venv venv
)

set PYTHON="venv\Scripts\Python.exe"

: have fun :)
%PYTHON% .\_requirements.py

: have fun :)
%PYTHON% .\main.py

pause
