import subprocess
import sys

try:
    import main
    from files.SANP_DOCS import launch
    from src import *
    from utils import *
except ModuleNotFoundError:
    print("检测到是首次启动, 开始安装所需依赖...")
    subprocess.call(f"{sys.executable} -s -m pip install -r requirements.txt")
