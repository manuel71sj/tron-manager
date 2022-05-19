import configparser
import os

SERVER_TYPE = "local"

config = configparser.ConfigParser()

config_dir = os.path.dirname(os.path.abspath(__file__))
config.read(os.path.join(config_dir, "config_%s.ini" % SERVER_TYPE))

DEFAULT = dict()
for (k, v) in config.items("DEFAULT"):
    DEFAULT[k] = v

MONGODB = dict()
for (k, v) in config.items("MongoDB"):
    MONGODB[k] = v

MARIADB = dict()
for (k, v) in config.items("MariaDB"):
    MARIADB[k] = v

TRON = dict()
for (k, v) in config.items("TRON"):
    TRON[k] = v
