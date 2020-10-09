import re,os,time
from utils.readconfig import ReadConfig
from utils.myutils import MyUtils

class JDSpider:

    refine_cnt = 0
    def __init__(self):
        self.rc = ReadConfig()
        self.utils = MyUtils()
        self.root_path = self.rc.get_value('root_folder','input') + '\\' + self.rc.get_value('sub_folder','jd')
        self.filename = 'jd_' + str(int(time.strftime("%Y%m%d%H%M"))) + '.csv'
        self.jd_output = self.rc.get_value('root_folder','output') + '\\' + self.rc.get_value('sub_folder','jd') + '\\' + self.filename
        self.root_pattern = r'<span class="dealtime" title=[\s\S]*?<div class="pagin fr">'

    def __update_filename(self):
        self.rc.set_value('file_name','jd_file', self.filename)
        self.rc.write_config(open(ReadConfig.configpath, "w"))

# 获取html文本内容
    def __fetch_content(self,file):
        with open(self.root_path + '\\' + file , 'r', encoding='utf-8') as f:
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
                refined_anchor = ['']
                JDSpider.refine_cnt += 1
                anchor['id'] = str(JDSpider.refine_cnt)
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
                refined_anchor.append(anchor['dealtime'][0])
                refined_anchor.append(anchor['pay_pattern'][0])
                refined_anchor.append(anchor['order_shop'])
                refined_anchor.append(anchor['product'])
                refined_anchor.append(-1 * float(anchor['amount'][0]))
                refined_anchor.append(anchor['order_status'])
                refined_anchor.append('')
                refined_anchor.append('')
                refined_anchor.append('京东')
                refined_anchors.append(refined_anchor)
            # a = 1
        return refined_anchors

    def __spider_go(self):
        self.__update_filename()
        files = os.listdir(self.root_path)
        for file in files:
            html = self.__fetch_content(file)
            raw_anchors = self.__analysis(html)
            refined_anchors = self.__refine_data(raw_anchors)
            self.utils.write_csv_append(self.jd_output,refined_anchors)
        print('【京东】共采集['+ str(JDSpider.refine_cnt) + ']条数据')

    def jd_go(self):
        self.__spider_go()
        new_utils = MyUtils()
        jd_outpath = new_utils.get_outpath('jd')
        if os.path.exists(jd_outpath):
            print('【京东】清洗后数据已保存成功！保存路径为' + jd_outpath)

# if __name__ == '__main__':
#     ms = MyJDSpider()
#     ms.spider_go()

