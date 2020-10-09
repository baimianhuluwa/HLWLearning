from utils.readconfig import ReadConfig
import os
import xlrd
import unicodecsv as ucsv
import csv
import time

class MyUtils:
    def __init__(self):
        self.rc = ReadConfig()

    def get_filename(self,param):
        filename = self.rc.get_value('file_name',param + '_file')
        return filename

    def get_inpath(self,param):
        input_root = self.rc.get_value('root_folder','input')
        input_folder = os.path.join(input_root,self.rc.get_value('sub_folder',param))
        filename = self.get_filename(param)
        inpath = os.path.join(input_folder,filename)
        return inpath

    def get_outpath(self,param):
        output_root = self.rc.get_value('root_folder','output')
        output_folder = os.path.join(output_root, self.rc.get_value('sub_folder', param))
        filename = self.get_filename(param).split('.')[0] + '.csv'
        outpath = os.path.join(output_folder,filename)
        return outpath

    def get_union_outpath(self):
        union_folder = self.rc.get_value('root_folder','output')
        filename = 'union_' + str(int(time.strftime("%Y%m%d%H%M"))) + '.csv'
        union_outpath = os.path.join(union_folder,filename)
        return union_outpath

    def read_xls(self,inpath):
        wb = xlrd.open_workbook(inpath)
        sht = wb.sheet_by_index(0)
        return sht

    def read_gbk_csv(self,inpath):
        with open(inpath,'r',encoding='gbk') as f:
            reader = csv.reader(f)
            result = list(reader)
        return result

    def read_utf_csv(self,inpath):
        with open(inpath,'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            result = list(reader)
        return result

    # def write_gbk_csv(self,outpath,data):
    #     with open(outpath,'wb') as f:
    #         writer = ucsv.writer(f,encoding='gbk')
    #         writer.writerows(data)

    def write_csv(self,outpath,data):
        with open(outpath,'wb') as f:
            writer = ucsv.writer(f,encoding='utf-8-sig')
            writer.writerows(data)

    def write_csv_append(self,outpath,data):
        with open(outpath,'ab') as f:
            writer = ucsv.writer(f,encoding='utf-8-sig')
            writer.writerows(data)

    def sort_by_goods(self,data_source,goods_name):
        sort = ''
        goods_keywds = self.rc.get_keywds(data_source)
        for keywd in goods_keywds.items():
            words = keywd[1].split(",")
            for word in words:
                if word in goods_name:
                    sort = keywd[0]
        return sort


if __name__ == '__main__':
    utils = MyUtils()
    inpath = utils.get_inpath('ccb_credit')
    outpath = utils.get_outpath('ccb_credit')
    print(inpath)
    print(outpath)
# csv测试
    result = utils.read_gbk_csv(inpath)
    print(result)
    # print(len(result))

# # excel测试
#     sht = utils.read_xls(inpath)
#     # s = sht.cell(0,0).value
#     # print(s)
#     data_list = []
#     # r1 = sht.row_values(5)
#     r2 = sht.row_values(5)
#     print(r2)
#     rows = sht.nrows
#     cols = sht.ncols
#     # print(rows,cols)
#     # data_list.append(r1)
#     # data_list.append(r2)
#     # utils.write_csv(outpath,data_list)
#     data_row = []
#     old_date = str(r2[0])
#     # print(trade_date)
#     new_time = old_date[0:4] + '-' + old_date[4:6] + '-' + old_date[-2:] + ' 05:20:00'
#     print(new_time)
#     if len(r2[1]) == 0:
#         r2[1] = 0.0
#     if len(r2[2]) == 0:
#         r2[2] = 0.0
#     amount = float(r2[2]) + (-1) * float(r2[1])
#     print(amount)