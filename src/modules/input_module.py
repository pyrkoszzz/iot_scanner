import json


class InputHandler:
    def __init__(self, config_file="config/settings.json"):
        self.config_file = config_file

    def get_ip_ranges(self):
        with open(self.config_file, "r") as file:
            settings = json.load(file)
        return settings.get("ip_ranges", [])
