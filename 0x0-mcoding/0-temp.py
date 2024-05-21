#!/usr/bin/env python3
import logging.config
import json
import os
logger = logging.getLogger("0-app-lig")
logging = logging.config
logging_config = {
    "version":1, "disable_existing_loggers":False,
    "formatters":{
        "simple":{
            "format":"%(levelname)s:  %(message)s",
        }
    },
    "handlers":{
        "stdout":"logging.StreamHandler",
        "formatter":"simple",
        "stream":"ext://sys.stdout",
    },
    "logger":{
        "root":{"lever":"DEBUG", "handlers":["stdout"]}
        },
}
print(logging)
print("Current working directory:", os.getcwd())
with open('config.json', 'r') as file:
    config = json.load(file)