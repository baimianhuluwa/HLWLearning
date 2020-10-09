from utils.myutils import MyUtils
from account.alipay import Alipay
from account.wechat import Wechat
from account.ccbdebit import CCBDebit
from account.ccbcredit import CCBCredit
from account.cmbcdebit import CMBCDebit
from account.jdspider import JDSpider

class SortMyAccount:

    def __init__(self):
        self.ali = Alipay()
        self.wc = Wechat()
        self.ccbd = CCBDebit()
        self.ccbc = CCBCredit()
        self.cmbc = CMBCDebit()
        self.jd = JDSpider()
        self.utils = MyUtils()

# 分别清洗各个账户的数据
    def refine_all(self):
    # 支付宝
        self.ali.alipay_go()
    # 微信
        self.wc.wechat_go()
    # 建行借记卡
        self.ccbd.ccb_debit_go()
    # 建行信用卡
        self.ccbc.ccb_credit_go()
    # 民生借记卡
        self.cmbc.cmbc_debit_go()
    # 京东
        self.jd.jd_go()
# 将所有数据合并在一个文件中
    def union_all(self):
        res_lists = []
    # 支付宝
        alipay_res = self.utils.read_utf_csv(self.ali.alipay_outpath)
        res_lists.append(alipay_res)
    # 微信
        wechat_res = self.utils.read_utf_csv(self.wc.wechat_outpath)
        res_lists.append(wechat_res)
    # 建行借记卡
        ccb_debit_res = self.utils.read_utf_csv(self.ccbd.ccb_debit_outpath)
        res_lists.append(ccb_debit_res)
    # 建行信用卡
        ccb_credit_res = self.utils.read_utf_csv(self.ccbc.ccb_credit_outpath)
        res_lists.append(ccb_credit_res)
    # 民生借记卡
        cmbc_debit_res = self.utils.read_utf_csv(self.cmbc.cmbc_debit_outpath)
        res_lists.append(cmbc_debit_res)
    # 京东
        new_utils = MyUtils()
        jd_outpath = new_utils.get_outpath('jd')
        # print(jd_outpath)
        jd_res = self.utils.read_utf_csv(jd_outpath)
        res_lists.append(jd_res)
    # 合并
        union_outpath = self.utils.get_union_outpath()
        for res in res_lists:
            self.utils.write_csv_append(union_outpath, res)

if __name__ == '__main__':
    smc = SortMyAccount()
    smc.refine_all()
    smc.union_all()
    # smc.ali.alipay_go()
    # smc.wc.wechat_go()
    # smc.ccbd.ccb_debit_go()
    # smc.cmbc.cmbc_debit_go()







