import configparser

config = configparser.ConfigParser()


def config_init(path):
    config.read(path)
