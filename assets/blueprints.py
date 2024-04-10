import json


def config_blueprint():
    config_layout = {"Token": ""}
    json_obj = json.dumps(config_layout, indent=4)
    return json_obj


def data_blueprint():
    data_str = [{"typ": "default_roles", "default_roles": []}, {"typ": "news_channel", "id": ""},
                {"type": "reaction_channel", "id": ""}, {"type": "Admin", "roles": []}]

