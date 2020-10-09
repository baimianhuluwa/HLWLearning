from JdSpider.NewConfigParser import NewConfigParser
import os

class ReadConfig:
    root_dir = os.getcwd()
    configpath = os.path.join(root_dir, "config.ini")
    def __init__(self):
        self.conf = NewConfigParser()
        # print('配置文件路径为：' + configpath)
        self.conf.read(ReadConfig.configpath,encoding='utf-8')

    def get_dbinfo(self,param):
        value = self.conf.get('mysql',param)
        return value

    def get_header(self):
        header_info = {}
        headers = self.conf.items('header')
        for header in headers:
            header_info[header[0]] = header[1]
        return header_info

    # def get_cookie(self):
    #     cookie_dict = {}
    #     cookies = self.conf.items('cookies')
    #     for cookie in cookies:
    #         cookie_dict[cookie[0]] = cookie[1]
    #     return cookie_dict

    def get_cookie(self):
        cookie_dict = {}
        cookies = self.conf.get('cookies','cookie')
        ck_list = cookies.split('; ')
        for ck in ck_list:
            cookie_dict[ck.split('=')[0]] = ck.split('=')[1]
        return cookie_dict

    def get_url(self,param):
        value = self.conf.get('url',param)
        return value

    def get_value(self,section,param):
        value = self.conf.get(section,param)
        return value

    def set_value(self,section,option,value):
        self.conf.set(section,option,value)

    def write_config(self,fp):
        self.conf.write(fp)

# if __name__ == '__main__':
#     rc = ReadConfig()
    # print(rc.get_value('cookies', 'cookie'))
    # print(rc.get_cookie())
#     # print(rc.get_headerinfo())
#     port = int(rc.get_dbinfo('port'))
#     print(port)
#     print(type(port))
#     # print(rc.get_url('url','loco_url'))
#     # print(rc.get_url('url', 'ovld_url_sec'))
#     # print(rc.get_url('url', 'imba_url_sec'))
