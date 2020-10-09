# 从selenium导入webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from loco_alarm_spider.ReadConfig import ReadConfig
import time

class GetCookies:
    def __init__(self):
        self.rc = ReadConfig()
        self.chromedriver = self.rc.get_value('chrome','chromedriver')
        # 这个是一个用来控制chrome以无界面模式打开的浏览器
        # 创建一个参数对象，用来控制chrome以无界面的方式打开
        self.chrome_options = Options()
        # 后面的两个是固定写法 必须这么写
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(executable_path=self.chromedriver,chrome_options=self.chrome_options)
        self.log_url = self.rc.get_url('log_url')
        self.username = self.rc.get_value('loginfo','username')
        self.password = self.rc.get_value('loginfo','password')

    def update_cookies(self):
        self.browser.get(self.log_url)
        # 找到用户名输入框
        usernameInput = self.browser.find_element_by_name('username')
        # 输入用户名
        usernameInput.send_keys(self.username)
        # 稍等1s
        # time.sleep(1)
        # 找到密码输入框
        passwdInput = self.browser.find_element_by_name('password')
        # 输入密码
        passwdInput.send_keys(self.password)
        # 稍等1s
        # time.sleep(1)
        # 找到登录按钮
        loginButton = self.browser.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[1]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input[1]')
        # 单击登录按钮
        loginButton.click()
        # 稍等1s
        # time.sleep(1)
        # 单击'浏览近期列车'
        browseButton = self.browser.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/div[1]/a[2]')
        browseButton.click()
        #获取cookie
        cookie_items = self.browser.get_cookies()
        # print(cookie_items)
        # 将获取的cookie更新到config.ini文件中
        for cookie in cookie_items:
            self.rc.set_value('cookies',cookie.get('name'),cookie.get('value'))
            self.rc.write_config(open(ReadConfig.configpath, "w"))

    def driver_quit(self):
        self.browser.quit()
        print('浏览器已退出')


        #组装cookie字符串
        # cookies = {}
        # for cookie in cookie_items:
        #     cookies[cookie.get('name')] = cookie.get('value')
        # #打印出来看一下
        # print(cookies)
