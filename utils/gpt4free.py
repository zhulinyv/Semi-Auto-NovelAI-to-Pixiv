from g4f.gui import run_gui

from utils.env import env


def main():
    run_gui(port=env.g4f_port)
