import os
import sys

from g4f.gui import run_gui

from utils.env import env


def main():
    if env.skip_else_log:
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
    run_gui(port=env.g4f_port)
