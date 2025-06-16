import configparser
import os

def get_config_value(section, key):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '../configFiles/LIYA Crafter Test Details.ini')
    config.read(config_path)
    return config.get(section, key)