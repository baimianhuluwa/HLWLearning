from utils.myutils import MyUtils
import os

class CMBCDebit:
    cmbc_debit_cnt = 0

    def __init__(self):
        self.utils = MyUtils()
        self.cmbc_debit_inpath = self.utils.get_inpath('cmbc_debit')
        self.cmbc_debit_outpath = self.utils.get_outpath('cmbc_debit')

# 清洗数据
    def __refine_cmbc_debit(self, inpath):
        raw_sht = self.utils.read_xls(inpath)
        used_rows = raw_sht.nrows
        data_rows = []
        for i in range(4, used_rows):
            raw_row = raw_sht.row_values(i)
            data_row = ['']
            old_date = str(raw_row[0])
            new_time = old_date[0:4] + '-' + old_date[4:6] + '-' + old_date[-2:] + ' 05:20:00'
            if len(raw_row[1]) == 0:
                raw_row[1] = 0.0
            if len(raw_row[2]) == 0:
                raw_row[2] = 0.0
            amount = float(raw_row[2]) + (-1) * float(raw_row[1])
            sort = self.utils.sort_by_goods('cmbc_debit', raw_row[8])
            data_row.append(new_time)
            data_row.append(raw_row[7])
            data_row.append(raw_row[5])
            data_row.append(raw_row[8])
            data_row.append(amount)
            data_row.append('')
            data_row.append(raw_row[6])
            data_row.append(sort)
            data_row.append('民生借记卡')
            # print(data_row)
            data_rows.append(data_row)
            CMBCDebit.cmbc_debit_cnt += 1
        print('【民生借记卡】共采集[' + str(CMBCDebit.cmbc_debit_cnt) + ']条数据')
        return data_rows

    # 清洗后的数据写入csv文件
    def cmbc_debit_go(self):
        cmbc_debit_data = self.__refine_cmbc_debit(self.cmbc_debit_inpath)
        self.utils.write_csv(self.cmbc_debit_outpath, cmbc_debit_data)
        if os.path.exists(self.cmbc_debit_outpath):
            print('【民生借记卡】清洗后数据已保存成功！保存路径为' + self.cmbc_debit_outpath)