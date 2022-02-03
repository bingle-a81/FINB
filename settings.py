# -*- coding: utf-8 -*-
import logging


class MegaHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename

    def emit(self, record):
        message = self.format(record)
        with open(self.filename, 'a') as file:
            file.write(message + '\n')


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'std_format'
        },
        'file': {
            '()': MegaHandler,
            'level': 'INFO',
            'filename': 'C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log',
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
            #'propagate': False
        }
    }
    # 'filters': {
    #   'color':{
    #       "DEBUG": "GREEN",
    #       "INFO": "GREEN",
    #       "WARNING": "YELLOW",
    #       "ERROR": "RED",
    #       "CRITICAL": "RED"
    #   }
    #
    # }
    # 'root': {}   # '': {}
    # 'incremental': True
}

