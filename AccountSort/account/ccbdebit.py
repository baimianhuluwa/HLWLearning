from utils.myutils import MyUtils
import os


class CCBDebit:
    ccb_debit_cnt = 0

    def __init__(self):
        self.utils = MyUtils()
        self.ccb_debit_inpath = self.utils.get_inpath('ccb_debit')
        self.ccb_debit_outpath = self.utils.get_outpath('ccb_debit')

    # 清洗数据
    def __refine_ccb_debit(self, inpath):
        raw_sht = self.utils.read_xls(inpath)
        used_rows = raw_sht.nrows
        data_rows = []
        for i in range(6, used_rows - 1):
            raw_row = raw_sht.row_values(i)
            data_row = ['']
            old_date = str(raw_row[1])
            new_time = old_date[0:4] + '-' + old_date[4:6] + '-' + old_date[-2:] + ' ' + str(raw_row[2])
            amount = float(raw_row[4]) + (-1) * float(raw_row[3])
            sort = self.utils.sort_by_goods('ccb_debit', raw_row[10])
            data_row.append(new_time)
            data_row.append(raw_row[7])
            data_row.append(raw_row[9])
            data_row.append(raw_row[10])
            data_row.append(amount)
            data_row.append('')
            data_row.append('')
            data_row.append(sort)
            data_row.append('建行借记卡')
            # print(data_row)
            data_rows.append(data_row)
            CCBDebit.ccb_debit_cnt += 1
        print('【建行借记卡】共采集[' + str(CCBDebit.ccb_debit_cnt) + ']条数据')
        return data_rows

    # 清洗后的数据写入csv文件
    def ccb_debit_go(self):
        ccb_debit_data = self.__refine_ccb_debit(self.ccb_debit_inpath)
        self.utils.write_csv(self.ccb_debit_outpath, ccb_debit_data)
        if os.path.exists(self.ccb_debit_outpath):
            print('【建行借记卡】清洗后数据已保存成功！保存路径为' + self.ccb_debit_outpath)