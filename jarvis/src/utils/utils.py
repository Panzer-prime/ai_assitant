import json
from src.plugin.load_plugins import load_plugins

def write_in_json(obj):
    with open("jarvis/assets/plugins_metadata.json", 'w') as file:
       json_obj = json.dumps(obj, indent=4)
       file.write(json_obj)


def create_available_functions():
    plugins = load_plugins()
    available = {}
    for plugin in plugins: 
        available[plugin.name] = plugin.run
    return available

