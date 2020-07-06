import json

configuration = {}

def read_config():
    global configuration
    with open('dada_config.json') as configfile:
        configuration = json.load(configfile)
