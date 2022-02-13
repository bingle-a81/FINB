# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler, Formatter, LogRecord

class MegaHandler(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)
        self.filename = filename

    def emit(self, record):
        message = self.format(record)
        with open(self.filename, 'a') as file:
            file.write(message + '\n')


# class CustomFilter(logging.Filter):
#     def filter(self, record):
#         # print(dir(record))
#         # print(record.new_name)
#         return record.funcName == 'new_function'



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
            'formatter': 'std_format',
            # 'filters': ['new_filter'],
        },
        'file': {
            '()': MegaHandler,
            'level': 'INFO',
            'filename': 'C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log',
            'formatter': 'std_format',

        },
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            # 'propagate': False
        },
        'json_logger': {
            'level': 'DEBUG',
            'handlers': ['console'],


            # 'propagate': False
        },

    },
    # 'filters': {
    #     'new_filter': {
    #         '()': CustomFilter,
    #     }
    # },

}

# },
# 'filters': {
#     'addFilter':CastormFilter
# },
#
# }
# 'root': {}   # '': {}
# 'incremental': True
# class CastormFilter(logging.Filter):
#     COLOR = {
#         'DEBUG': "GREEN",
#         "INFO": "YELLOW",
#         'ERROR': 'RED',
#         'CRITICAL': 'RED'
#     }