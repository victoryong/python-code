# coding: utf-8

__author__ = 'Victor Y, Xie'


import time


loggers = {}


class LoggerPrinter:
    def __init__(self, name):
        self.name = name

    def info(self, text):
        print(f'{time.asctime()} [{self.name}] - [INFO] {text}')

    def error(self, text):
        print(f'{time.asctime()} [{self.name}] - [ERROR] {text}')

    def debug(self, text):
        print(f'{time.asctime()} [{self.name}] - [DEBUG] {text}')

    def warn(self, text):
        print(f'{time.asctime()} [{self.name}] - [WARN] {text}')


def get_or_create_logger(name):
    return loggers.get(name, LoggerPrinter(name))


if __name__ == '__main__':
    logger = get_or_create_logger('test')
    logger.info('test info')
    logger.error('test error')
    logger.debug('test debug')
    logger.warn('test warn')
