



def write_in_json(obj):
    with open("jarvis/assets/plugins_metadata.json", 'w') as file:
       json_obj = json.dumps(obj, indent=4)
       file.write(json_obj)


def create_metadata_file(plugins):
    metadata = {}
    for plugin in plugins: 
        metadata[plugin.name] = plugin.description

    
    write_in_json(metadata)