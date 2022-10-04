import json

class ConfigManager:
    def __init__(self, filename) -> None:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
            self.configs = data

    def get_configs(self):
        return self.configs

if __name__ == "__main__":
    ConfigManager('config_sample.json')