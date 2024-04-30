import importlib.util
import os


def load_plugins(directory):
    plugins = {}
    plugin_list = os.listdir(directory)
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
