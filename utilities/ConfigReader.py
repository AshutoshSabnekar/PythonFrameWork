import configparser
import os

def get_config_value(section, key):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '../configFiles/LIYA Crafter Test Details.ini')
    print("Resolved config path:", config_path)
    config.read(config_path, encoding='utf-8')

    if config.has_section(section):
        return config.get(section, key)
    else:
        raise ValueError(f"Section '{section}' not found in config file.")
