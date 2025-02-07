import os
import sys

from mkdocs.__main__ import cli

from utils.env import env


def main():
    if env.skip_else_log:
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
    os.chdir("./files/SANP_DOCS")
    cli(["serve"])
