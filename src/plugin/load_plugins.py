import importlib.util
import os
import importlib
import inspect
from src.plugin.base_plugin import BasePluging
PLUGIN_PATH = "src/plugin"


def load_plugins():
    plugins = []
    for root, folders, files in os.walk(PLUGIN_PATH):
        for file in files:
            if not file.endswith("py"):
                continue


            filepath = os.path.join(root, file)
            module_name = filepath[:-3]
            print(module_name)


            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BasePluging) and obj is not BasePluging:
                    plugins.append(obj())



    return plugins

