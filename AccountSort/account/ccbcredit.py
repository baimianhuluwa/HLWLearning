from utils.myutils import MyUtils
import os


class CCBCredit:
    ccb_credit_cnt = 0

    def __init__(self):
        self.utils = MyUtils()
        self.ccb_credit_inpath = self.utils.get_inpath('ccb_credit')
        self.ccb_credit_outpath = self.utils.get_outpath('ccb_credit')

# 清洗数据
    def __refine_ccb_credit(self, inpath):
        raw_data = self.utils.read_gbk_csv(inpath)
        data_rows = []
        for i in range(15, len(raw_data)):
            raw_row = raw_data[i]
            data_row = ['']
            if len(raw_row) != 0:
                old_date = str(raw_row[1].strip())
                new_time = old_date[0:4] + '-' + old_date[4:6] + '-' + old_date[-2:] + ' 05:20:00'
                amount = -1 * float(raw_row[5])
                data_row.append(new_time)
                data_row.append('ETC')
                data_row.append('')
                data_row.append(raw_row[6])
                data_row.append(amount)
                data_row.append('')
                data_row.append('')
                if amount < 0:
                    data_row.append('汽车')
                else:
                    data_row.append('资金转移')
                data_row.append('建行信用卡')
                # print(data_row)
                data_rows.append(data_row)
                CCBCredit.ccb_credit_cnt += 1
        print('【建行信用卡】共采集[' + str(CCBCredit.ccb_credit_cnt) + ']条数据')
        return data_rows

# 清洗后的数据写入csv文件
    def ccb_credit_go(self):
        ccb_credit_data = self.__refine_ccb_credit(self.ccb_credit_inpath)
        self.utils.write_csv(self.ccb_credit_outpath, ccb_credit_data)
        if os.path.exists(self.ccb_credit_outpath):
            print('【建行信用卡】清洗后数据已保存成功！保存路径为' + self.ccb_credit_outpath)