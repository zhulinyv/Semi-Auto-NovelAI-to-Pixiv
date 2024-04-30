import importlib.util
import os


def load_plugins(directory):
    plugins = {}
    for root, dirs, files in os.walk(directory):
        try:
            for dir in dirs:
                if dir == "__pycache__":
                    pass
                else:
                    plugin_name = dir
                    module_name = f"{directory}.{dir}"
                    spec = importlib.util.spec_from_file_location(
                        module_name, os.path.join(directory, dir, "__init__.py")
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugins[plugin_name] = module
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    plugin_name = os.path.splitext(file)[0]
                    module_name = f"{directory}.{plugin_name}"
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugins[plugin_name] = module
        except FileNotFoundError:
            pass
    return plugins
