import configparser
import os

SERVER_TYPE = "local"

config = configparser.ConfigParser()

config_dir = os.path.dirname(os.path.abspath(__file__))
config.read(os.path.join(config_dir, "config_%s.ini" % SERVER_TYPE))


def collect_item(name: str) -> dict:
    temp = dict()
    for (k, v) in config.items(name):
        temp[k] = v

    return temp


DEFAULT = collect_item("DEFAULT")
MONGODB = collect_item("MongoDB")
MARIADB = collect_item("MariaDB")
TRON = collect_item("TRON")
OutSite = collect_item("OutSite")

# DEFAULT = dict()
# for (k, v) in config.items("DEFAULT"):
#     DEFAULT[k] = v
#
# MONGODB = dict()
# for (k, v) in config.items("MongoDB"):
#     MONGODB[k] = v
#
# MARIADB = dict()
# for (k, v) in config.items("MariaDB"):
#     MARIADB[k] = v
#
# TRON = dict()
# for (k, v) in config.items("TRON"):
#     TRON[k] = v
#
# OutSite = dict()
# for (k, v) in config.items("OutSite"):
#     OutSite[k] = v
