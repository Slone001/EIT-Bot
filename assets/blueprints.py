import json


def config_blueprint():
    config_layout = {"Token": ""}
    json_obj = json.dumps(config_layout, indent=4)
    return json_obj


def data_blueprint() -> list:
    data_str = [{"typ": "default_roles", "roles": []}, {"typ": "admin_roles", "roles": []},
                {"typ": "news_channel", "id": ""}, {"typ": "reaction_channel", "id": ""},
                {"typ": "log_channel", "id": ""}]
    return data_str
