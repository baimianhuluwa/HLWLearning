# # 读取配置文件
# from NewConfigParser import NewConfigParser
#
# config = NewConfigParser()
# configpath = r'C:\Users\ZouHan\Work\02 培训资料\慕课\python\zhtest\config.ini'
# config.read(configpath,encoding='utf-8')
# a = config.get("cookies","JSESSIONID")
# print(a)
# print(type(a))
#
# # 修改配置文件内容
# # config.add_section("book")
# # config.set("book", "title", "the python standard library")
# # config.set("book", "author", "fredrik lundh")
# # config.set("cookies", "JSESSIONID", '2222222')
# # write to file
# # config.write(open(configpath, "w")) # 没有新建  存在打开
import pymysql
import re

filepath = r'C:\Users\ZouHan\Life\建行账单\CCB_0828.txt'
with open(filepath, 'r',encoding='utf-8') as f:  # 打开文件
    lines = f.readlines()  # 读取文件

conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'mysql',
    db = 'zouhan',
    charset = 'utf8'
)
cur = conn.cursor()

for line in lines:
    data_list = line.strip('\n').split("\t")
    time_str = data_list[2]
    data_list[2] = time_str[0:4] + '-' + time_str[4:6] + '-' + time_str[6:8]
    data_list[3] = re.sub(',','',data_list[3])
    data_list[4] = re.sub(',', '', data_list[4])
    # print(len(data_list))
    trade_shop = data_list[5] if len(data_list) == 6 else " "
    if '支付宝' in trade_shop:
        pay_pattern = '支付宝'
    elif '微信' in trade_shop:
        pay_pattern = '微信'
    elif '京东' in trade_shop:
        pay_pattern = '京东'
    else:
        pay_pattern = ' '
    sql = "insert into zouhan.ccb (id,trade_date,trade_time,amount,trade_balance,trade_shop,trade_type,pay_pattern,remarks,sort) values (" + data_list[0] +"," + "'" + data_list[2] + "'" +"," + "'" + data_list[2] + " 05:20:00'" + "," + data_list[3] + "," + data_list[4] + "," + "'" + trade_shop + "'" + "," + "'" + data_list[1] + "'," +  "'" + pay_pattern + "'," + "' '," + "' ');"

    cur.execute(sql)
    conn.commit()

