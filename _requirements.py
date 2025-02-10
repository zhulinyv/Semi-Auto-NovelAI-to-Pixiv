import subprocess
import sys

try:
    import main  # noqa
    from files.SANP_DOCS import launch  # noqa
    from src import *  # noqa
    from utils import *  # noqa
except ModuleNotFoundError:
    print("检测到是首次启动, 开始安装所需依赖...")
    subprocess.call(f"{sys.executable} -s -m pip install -r requirements.txt")
