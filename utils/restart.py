import os
import sys


def restart():
    p = sys.executable
    os.execl(p, p, *sys.argv)
