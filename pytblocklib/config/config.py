import configparser
import os
CONFIG_PATH = 'config.ini'

DEFAULT_CONTENT = '''[DEFAULT]
#1:Chrome, 2:Firefox
browser = 1
'''


def get_env():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH,encoding='utf-8',mode='w') as f:
            f.write(DEFAULT_CONTENT)
            f.flush()
    config.read(CONFIG_PATH)
    conf_def = config['DEFAULT']
    browser = conf_def.get('browser')
    return browser