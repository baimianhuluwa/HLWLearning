import re
import os
from JdSpider.ReadConfig import ReadConfig
from JdSpider.HandleDB import HandleDB

class MySpider:

    refine_cnt = 0
    def __init__(self):
        self.rc = ReadConfig()
        self.db = HandleDB()
        self.root_path = 'C:\\Users\\ZouHan\\Life\\记账-20200901之后\\原始账单\\京东'
        self.root_pattern = r'<span class="dealtime" title=[\s\S]*?<div class="pagin fr">'

# 获取html文本内容
    def __fetch_content(self,file):
        with open(self.root_path + file , 'r', encoding='utf-8') as f:
            html = str(re.findall(self.root_pattern,f.read()))
        return html
# 解析html文件
    def __analysis(self,html):
        # 正则匹配规则
        line_pattern = r'<span class="dealtime" title=[\s\S]*?</tbody>'
        dealtime_pattern = r'<span class="dealtime" title="([\s\S]*?)">'
        order_num_pattern = r'order_num">([\s\S]*?)</a>'
        order_shop_pattern = r'vender" title="([\s\S]*?)">'
        product_pattern = r'order_product" target="_blank" title="([\s\S]*?)">'
        goods_number_pattern = r'<div class="goods-number">([\s\S]*?)</div>'
        pay_pattern = r'<span class="ftx-13">([\s\S]*?)</span>'
        amount_pattern = r'<span>¥([\s\S]*?)</span>'
        order_status_pattern = r'<span class="order-status ftx-03">([\s\S]*?)</span>'
        lines = re.findall(line_pattern,html)
        raw_anchors = []
        for line in lines:
            raw_anchor = {
                'dealtime': re.findall(dealtime_pattern,line),
                'order_num':re.findall(order_num_pattern,line),
                'order_shop':re.findall(order_shop_pattern,line),
                'product':re.findall(product_pattern,line),
                'goods_number':re.findall(goods_number_pattern,line),
                'pay_pattern':re.findall(pay_pattern,line),
                'amount':re.findall(amount_pattern,line),
                'order_status':re.findall(order_status_pattern,line)
            }
            raw_anchors.append(raw_anchor)
        return raw_anchors
# 精炼数据
    def __refine_data(self,anchors):

        refined_anchors = []
        for anchor in anchors:
            if len(anchor['amount']) != 0 :
                MySpider.refine_cnt += 1
                anchor['id'] = str(MySpider.refine_cnt)
                anchor['order_status'] = anchor['order_status'][0].replace('\\n','').replace('\\t','').strip()
                if len(anchor['order_shop']) == 0:
                    anchor['order_shop'] = '京东自营'
                else:
                    anchor['order_shop'] = anchor['order_shop'][0]
                if len(anchor['product']) != 0:
                    product_str = ''
                    products = anchor['product']
                    for product in products:
                        product_str += (product + ';')
                    anchor['product'] = product_str.rstrip(';')
                if len(anchor['goods_number']) != 0:
                    nums = anchor['goods_number']
                    total_num = 0
                    for num in nums:
                        new_num = int(re.sub('x','',num.replace('\\n','').strip()))
                        total_num += new_num
                    anchor['goods_number'] = str(total_num)
                refined_anchors.append(anchor)
        # print('清洗后得到[' + str(MySpider.refine_cnt) + ']条订单数据')
        return refined_anchors

# 订单数据入库
    def __dict2sql(self,anchors):
        for anchor in anchors:
            sql = ("""insert into zouhan.jd (id,trade_time,order_num,trade_shop,goods_name,
            goods_num,amount,pay_pattern,trade_status) values ("""
            + anchor['id'] +","
            + "'" + anchor['dealtime'][0] + "'" + ","
            + "'" + anchor['order_num'][0] + "'" + ","
            + "'" + anchor['order_shop'] + "'" + ","
            + "'" + anchor['product'] + "'" + ","
            + anchor['goods_number'] + ","
            + anchor['amount'][0] + ","
            + "'" + anchor['pay_pattern'][0] + "'" + ","
            + "'" + anchor['order_status'] + "');")
            print(sql)
            self.db.execute_sql(sql)

    def go(self):
        files = os.listdir(self.root_path)
        self.db.conn_db()
        for file in files:
            html = self.__fetch_content(file)
            raw_anchors = self.__analysis(html)
            refined_anchors = self.__refine_data(raw_anchors)
            self.__dict2sql(refined_anchors)
        self.db.commit_sql()
        self.db.close_conn()

