import json


def config_blueprint():
    config_layout = {"Token": ""}
    json_obj = json.dumps(config_layout, indent=4)
    return json_obj

