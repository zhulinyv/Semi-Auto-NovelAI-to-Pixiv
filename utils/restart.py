import os
import sys

from utils.prepare import logger


def restart():
    logger.warning("开始重启...")
    p = sys.executable
    os.execl(p, p, *sys.argv)
