from utils.newconfigparser import NewConfigParser
import os

class ReadConfig:
    root_dir = os.getcwd()
    # root_dir = r'C:\Users\ZouHan\Work\Python\zouhan'
    configpath = os.path.join(root_dir, "config.ini")
    def __init__(self):
        self.conf = NewConfigParser()
        # print('配置文件路径为：' + configpath)
        self.conf.read(ReadConfig.configpath,encoding='gbk')

    def get_dbinfo(self,param):
        value = self.conf.get('mysql',param)
        return value

    def get_value(self,section,param):
        value = self.conf.get(section,param)
        return value

    def set_value(self,section,option,value):
        self.conf.set(section,option,value)

    def write_config(self,fp):
        self.conf.write(fp)

    def get_keywds(self,data_source):
        keywds = {}
        words = self.conf.items(data_source + '_keywds')
        for word in words:
            keywds[word[0]] = word[1]
        return keywds


if __name__ == '__main__':
    rc = ReadConfig()
    kw = rc.get_keywds('alipay')
    print(kw)
    # print(rc.configpath)
#     print(rc.get_value('input_file_path','alipay_input'))

