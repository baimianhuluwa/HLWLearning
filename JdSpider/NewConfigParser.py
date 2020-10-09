import configparser

class NewConfigParser(configparser.RawConfigParser):

    def __init__(self, defaults=None):
        configparser.RawConfigParser.__init__(self, defaults=defaults)
    # 这里重写了optionxform方法，直接返回选项名
    def optionxform(self, optionstr):
        return optionstr