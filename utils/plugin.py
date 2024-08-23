import importlib.util
import os
import shutil
import sys

import requests

try:
    from git import Git
except Exception:
    os.environ["PATH"] = os.path.abspath("./Git23921/cmd")
    from git import Git

from utils.update import update
from utils.utils import file_path2list, proxies, read_json


def get_plugin_list():
    try:
        plugins: dict = requests.get(
            "https://raw.githubusercontent.com/zhulinyv/Semi-Auto-NovelAI-to-Pixiv/main/files/webui/plugins.json",
            proxies=proxies,
        ).json()
    except Exception:
        plugins: dict = read_json("./files/webui/plugins.json")
    return plugins


def load_plugins(directory):
    plugins = {}
    plugin_list = file_path2list(directory)
    # 示例插件和测试插件放到最后加载
    if "sanp_plugin_example" in plugin_list:
        plugin_list.remove("sanp_plugin_example")
        plugin_list.append("sanp_plugin_example")
    if "sanp_plugin_test.py" in plugin_list:
        plugin_list.remove("sanp_plugin_test.py")
        plugin_list.append("sanp_plugin_test.py")
    for plugin in plugin_list:
        if plugin.endswith(".py"):
            location = os.path.join(directory, plugin)
        elif plugin != "__pycache__":
            if os.path.exists(requirements_path := os.path.join(directory, plugin, "requirements.txt")):
                os.system(f"{sys.executable} -s -m pip install -r {requirements_path}")
            location = os.path.join(directory, plugin, "__init__.py")
        else:
            location = None
        if location:
            plugin_name = plugin
            module_name = f"{directory}.{plugin_name}"
            spec = importlib.util.spec_from_file_location(module_name, location)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            plugins[plugin_name] = module
    return plugins


def plugin_list():
    plugins = get_plugin_list()

    md = """| 名称(Name) | 类型(Type) | 描述(Description) | 仓库(URL) | 作者(Author) | 状态(Status) |
| :---: | :---: | :---: | :---: | :---: | :---: |
"""
    for plugin in list(plugins.keys()):
        if os.path.exists(
            "./plugins/{}/{}".format(
                plugins[plugin]["type"],
                plugins[plugin]["name"],
            )
        ):
            status = "已安装(Installed)"
        else:
            status = "未安装(Uninstalled)"
        md += "| {} | {} | {} | [{}]({}) | {} | {} |\n".format(
            plugins[plugin]["name"],
            plugins[plugin]["type"],
            plugins[plugin]["description"],
            plugins[plugin]["url"],
            plugins[plugin]["url"],
            plugins[plugin]["author"],
            status,
        )
    return md


def install_plugin(name):
    data = get_plugin_list()
    plugin_path = "./plugins/{}/{}".format(data[name]["type"], data[name]["name"])

    if os.path.exists(plugin_path):
        update("./plugins/{}/{}".format(data[name]["type"], data[name]["name"]))
        return "更新成功! 重启后生效!"

    Git().clone(data[name]["url"], plugin_path)

    return "安装成功! 重启后生效!"


def uninstall_plugin(name):
    data = get_plugin_list()
    shutil.rmtree("./plugins/{}/{}".format(data[name]["type"], data[name]["name"]))
