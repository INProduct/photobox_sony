import json
import os
import logger


class ConfigParser:

    @classmethod
    def read_config(cls):
        cls.config = None
        if 'config.json' in os.listdir():
            with open('config.json') as config_file:
                try:
                    cls.config = json.loads(config_file.read())
                    print(cls.config)
                except:
                    logger.Logger.write_error('can not read config file')
        else:
            cls._write_default_config()

    @classmethod
    def get_config_for(cls, key):
        val = cls.config.get(key) if cls.config else None
        if not val:
            logger.Logger.write_error('No value for ' + str(key) + ' found')
        return val

    @classmethod
    def write_config(cls):
        with open('config.json', 'w') as configfile:
            configfile.write(json.dumps(cls.config))

    @classmethod
    def _write_default_config(cls):
        jsonfile = {
            'debug': False,
            'debug_level': 3,
            'window_fullscreen': False,
            'window': {
                'height': 600,
                'width': 800,
                'start_point': {
                    'x': 0,
                    'y': 1,
                },
            },

        }
        with open('config.json', 'w') as configfile:
            configfile.write(json.dumps(jsonfile))

