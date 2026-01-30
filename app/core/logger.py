import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",  # o "json" si preferís JSON
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
            "formatter": "default",
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    },
}

import os
import copy

def init_logger():
    if os.getenv("ENV") == "test":
        # En entorno de test/CI, evitamos configurar el FileHandler
        # para no requerir directorios ni permisos de escritura.
        config = copy.deepcopy(LOGGING_CONFIG)
        
        # Remover handler 'file' si existe
        if "file" in config["handlers"]:
            del config["handlers"]["file"]
            
        # Remover 'file' de los handlers del root logger
        if "root" in config and "handlers" in config["root"]:
            config["root"]["handlers"] = [h for h in config["root"]["handlers"] if h != "file"]
            
        dictConfig(config)
    else:
        # En producción/dev, usamos la config completa con logs a archivo
        dictConfig(LOGGING_CONFIG)
