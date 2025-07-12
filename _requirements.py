import os
import shutil
import subprocess
import sys

from utils.env import env

try:
    os.remove("main.py")
except FileNotFoundError:
    pass

if env.new_interface:
    shutil.copyfile("./files/webui/main_new.py", "main.py")
else:
    shutil.copyfile("./files/webui/main_bak.py", "main.py")


try:
    import main  # noqa
    from files.SANP_DOCS import launch  # noqa
    from src import *  # noqa
    from utils import *  # noqa
except ModuleNotFoundError:
    print("检测到是首次启动, 开始安装所需依赖...")
    subprocess.call(f"{sys.executable} -s -m pip install -r requirements.txt")
