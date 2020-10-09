from utils.myutils import MyUtils
import os

class Alipay:
    alipay_cnt = 0

    def __init__(self):
        self.utils = MyUtils()
        self.alipay_inpath = self.utils.get_inpath('alipay')
        self.alipay_outpath = self.utils.get_outpath('alipay')

# 清洗数据
    def __refine_alipay(self, inpath):
        raw_data = self.utils.read_gbk_csv(inpath)
        data_rows = []
        for i in range(5, len(raw_data) - 7):
            raw_row = raw_data[i]
            data_row = ['']
            if '支出' in raw_row[10]:
                amount = -1 * float(raw_row[9])
            else:
                amount = float(raw_row[9])
            sort = self.utils.sort_by_goods('alipay',raw_row[8])
            data_row.append(raw_row[2])
            data_row.append(raw_row[5])
            data_row.append(raw_row[7])
            data_row.append(raw_row[8])
            data_row.append(amount)
            data_row.append(raw_row[11])
            data_row.append(raw_row[14])
            data_row.append(sort)
            data_row.append('支付宝')
            # print(data_row)
            data_rows.append(data_row)
            Alipay.alipay_cnt += 1
        print('【支付宝】共采集[' + str(Alipay.alipay_cnt) + ']条数据')
        return data_rows
# 清洗后的数据写入csv文件
    def alipay_go(self):
        alipay_data = self.__refine_alipay(self.alipay_inpath)
        self.utils.write_csv(self.alipay_outpath, alipay_data)
        if os.path.exists(self.alipay_outpath):
            print('【支付宝】清洗后数据已保存成功！保存路径为' + self.alipay_outpath)

