import configparser
import os

configfile_path = 'config.ini'

def get_env():
    config = configparser.ConfigParser()
    if not os.path.exists(configfile_path):
        raise FileNotFoundError(configfile_path)
    config.read(configfile_path)
    conf_def = config['DEFAULT']
    browser = conf_def.get('browser')
    return browser