Set objShell = CreateObject("WScript.Shell")
objShell.Run "venv\Scripts\Python.exe -m g4f.cli gui -port 19198 -debug", 0, False