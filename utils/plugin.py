import importlib.util
import os

from git import Git

from utils.utils import file_path2list, read_json


def load_plugins(directory):
    plugins = {}
    plugin_list = file_path2list(directory)
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
    plugins: dict = read_json("./files/webui/plugins.json")
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
    data = read_json("./files/webui/plugins.json")

    Git().clone(data[name]["url"], "./plugins/{}/{}".format(data[name]["type"], data[name]["name"]))

    return "安装成功! 重启后生效!"
