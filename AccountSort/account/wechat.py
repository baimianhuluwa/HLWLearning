from utils.myutils import MyUtils
import os


class Wechat:
    wechat_cnt = 0

    def __init__(self):
        self.utils = MyUtils()
        self.wechat_inpath = self.utils.get_inpath('wechat')
        self.wechat_outpath = self.utils.get_outpath('wechat')

    # 清洗数据
    def __refine_wechat(self, inpath):
        raw_data = self.utils.read_utf_csv(inpath)
        data_rows = []
        for i in range(17, len(raw_data)):
            raw_row = raw_data[i]
            data_row = ['']
            if '支出' in raw_row[4]:
                amount = -1 * float(raw_row[5].replace("¥", "").strip())
            else:
                amount = float(raw_row[5].replace("¥", "").strip())
            sort = self.utils.sort_by_goods('wechat', raw_row[3])
            data_row.append(raw_row[0])
            data_row.append(raw_row[1])
            data_row.append(raw_row[2])
            data_row.append(raw_row[3])
            data_row.append(amount)
            data_row.append(raw_row[7])
            data_row.append(raw_row[6])
            data_row.append(sort)
            data_row.append('微信')
            # print(data_row)
            data_rows.append(data_row)
            Wechat.wechat_cnt += 1
        print('【微信】共采集[' + str(Wechat.wechat_cnt) + ']条数据')
        return data_rows

    # 清洗后的数据写入csv文件
    def wechat_go(self):
        wechat_data = self.__refine_wechat(self.wechat_inpath)
        self.utils.write_csv(self.wechat_outpath, wechat_data)
        if os.path.exists(self.wechat_outpath):
            print('【微信】清洗后数据已保存成功！保存路径为' + self.wechat_outpath)