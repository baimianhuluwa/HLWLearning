import requests
import re
import time
from loco_alarm_spider.ReadConfig import ReadConfig
from loco_alarm_spider.HandleDB import HandleDB

class LocoAlarmSpider:
    # 计数
    loco_alarm_cnt = 0
    ovld_cnt = 0
    imba_cnt = 0

    def __init__(self):
        self.rc = ReadConfig()
        self.db = HandleDB()
        self.headers = self.rc.get_header()
        self.cookie = self.rc.get_cookie()
        self.loco_url = self.rc.get_url('loco_url')
        self.ovld_url_sec = self.rc.get_url('ovld_url_sec')
        self.imba_url_sec = self.rc.get_url('imba_url_sec')
        # 正则匹配规则
        self.root_pattern = r'<a href=\'[\s\S]*?<td align="center"></td></tr>'
        self.url_para_pattern = r"<a href='\?([\s\S]*?)'><img"
        self.line_pattern = r'<td[\s\S]*?</td>'
        self.ele_pattern1 = r'<td>([\s\S]*?)</td>'
        self.ele_pattern2 = r'<td class="numericMiddle">([\s\S]*?)</td>'
        self.ele_pattern3 = r"<div title='([\s\S]*?)' class='tooltip'"
        self.ele_pattern4 = r'<td style="color: red" align="center">([\s\S]*?)</td>'
        self.ele_pattern5 = r'<td>([\s\S]*)&nbsp;'
        self.ss = requests.Session()

# 获取html文本内容
    def __fetch_content(self,loco_alarm_url):
        res = self.ss.get(loco_alarm_url,headers=self.headers,cookies=self.cookie)
        htmls = res.text
        if "用户名 为必填项" in htmls:
            print('登录失败！请检查cookie是否正确')
            htmls = ''
        elif "确认所有搜索发现的报警" in htmls:
            print('登录成功！已进入机车告警界面')
        return htmls
# 解析html文件 
    def __analysis(self,htmls):
        lines = re.findall(self.root_pattern,htmls)
        raw_anchors = []
        for line in lines:
            url_paras = re.findall(self.url_para_pattern,line)[0].split('&amp;')
            eles = re.findall(self.line_pattern,line)
            raw_anchor = {
                'uuid': '',
                'overload_url':'',
                'imbalance_url':'',
                'trainDateTime':url_paras[0],
                'location':url_paras[1],
                'track':url_paras[2],
                'timeZone':url_paras[3],
                'train_order':eles[0],
                'alarm_time':eles[1],
                'station':eles[2],
                'track_num':eles[3],
                'direction':eles[4],
                'first_loco':eles[5],
                'velocity':eles[6],
                'total_loco':eles[9],
                'total_car':eles[11],
                'total_axis':eles[13],
                'total_weight':eles[15],
                'max_vertical_force':eles[18],
                'max_dynamic_load':eles[19],
                'max_ratio':eles[20],
                'max_transverse_stress':eles[21],
                'max_instability_index':eles[22],
                'train_warn':eles[23],
                'warn_confirm':eles[24]
            }
            raw_anchors.append(raw_anchor)
        print('共查询到[' + str(len(raw_anchors)) + ']条机车告警数据（包含未确认）')
        return raw_anchors
# 精炼机车报警数据
    def __refine_alarm(self,anchors):
        refine_cnt = 0
        refined_anchors = []
        for anchor in anchors:
            # confirm_tmp = re.findall(self.ele_pattern4,anchor['warn_confirm'])
            # if confirm_tmp:
            #     anchor['warn_confirm'] = re.findall(self.ele_pattern4,anchor['warn_confirm'])[0].strip()
            #     anchor['warn_confirm'] = confirm_info if 'value="确认"' not in confirm_info else '未确认'
            # else:
            #     anchor['warn_confirm'] = ''
            if '已确认' in anchor['warn_confirm']:
                anchor['warn_confirm'] = '已确认'
                anchor['train_order'] = re.findall(self.ele_pattern1,anchor['train_order'])[0].strip()
                tmp_alarm_time = re.findall(self.ele_pattern5,anchor['alarm_time'])[0].strip()
                anchor['alarm_time'] = re.sub(r"\s+","",tmp_alarm_time).replace('&nbsp;&nbsp;',' ')
                anchor['station'] = re.findall(self.ele_pattern1,anchor['station'])[0].strip()
                anchor['track_num'] = re.findall(self.ele_pattern1,anchor['track_num'])[0].strip()
                anchor['direction'] = re.findall(self.ele_pattern1,anchor['direction'])[0].strip()
                anchor['first_loco'] = re.findall(self.ele_pattern1,anchor['first_loco'])[0].strip()
                anchor['velocity'] = re.findall(self.ele_pattern2,anchor['velocity'])[0].strip()
                anchor['total_loco'] = re.findall(self.ele_pattern2,anchor['total_loco'])[0].strip()
                anchor['total_car'] = re.findall(self.ele_pattern2,anchor['total_car'])[0].strip()
                anchor['total_axis'] = re.findall(self.ele_pattern2,anchor['total_axis'])[0].strip()
                anchor['total_weight'] = re.findall(self.ele_pattern2,anchor['total_weight'])[0].strip().replace(",","")
                anchor['max_vertical_force'] = re.findall(self.ele_pattern2,anchor['max_vertical_force'])[0].strip()
                anchor['max_dynamic_load'] = re.findall(self.ele_pattern2,anchor['max_dynamic_load'])[0].strip()
                anchor['max_ratio'] = re.findall(self.ele_pattern2,anchor['max_ratio'])[0].strip()
                anchor['max_transverse_stress'] = re.findall(self.ele_pattern2,anchor['max_transverse_stress'])[0].strip()
                anchor['max_instability_index'] = re.findall(self.ele_pattern2,anchor['max_instability_index'])[0].strip()
                warn_tmp = re.findall(self.ele_pattern3,anchor['train_warn'])
                if warn_tmp:
                    anchor['train_warn'] = re.findall(self.ele_pattern3,anchor['train_warn'])[0].strip()
                else:
                    anchor['train_warn'] = ''
                anchor['uuid'] = re.sub(r"\D","",anchor['alarm_time']) + '_' + anchor['train_order'] + '_' + anchor['station'] + '_' + anchor['direction'] + '_' + anchor['track_num']
                anchor['overload_url'] = self.ovld_url_sec + anchor['track'] + '&' + anchor['trainDateTime'] + '&d-5711902-e=2&' + anchor['location'] + '&6578706f7274=1'
                anchor['imbalance_url'] = self.imba_url_sec + anchor['track'] + '&' + anchor['trainDateTime'] + '&' + anchor['location'] + '&6578706f7274=1&d-1190456-e=2'
                refined_anchors.append(anchor)
                refine_cnt += 1
        print('清洗后得到[' + str(refine_cnt) + ']条已确认的机车告警数据')
        return refined_anchors
# 读取偏载报告和超载报告数据，并做清洗
    def __fetch_report(self,report_url,uuid,train_order):
        report_res = self.ss.post(report_url,headers=self.headers,cookies=self.cookie)
        lines = report_res.text.split("\r\n")
        report = []
        if len(lines) != 0:
            # print('报告获取成功')
            month_dict = {
                '一月':'1','二月':'2','三月':'3','四月':'4','五月':'5','六月':'6',
                '七月':'7','八月':'8','九月':'9','十月':'10','十一月':'11','十二月':'12'
            }
            for i in range(1,len(lines)):
                line = lines[i].split("\t")
                new_line = [uuid,train_order,report_url]
                for ele in line:
                    tmp_ele = re.sub('[="]','',ele)
                    if '月' in tmp_ele:
                        time_list = tmp_ele.split(' ')
                        new_ele = time_list[0] + '|' + time_list[5] + '-' + month_dict[time_list[1]] + '-' + time_list[2] + ' ' + time_list[3]
                    elif len(tmp_ele) > 0:
                        new_ele = tmp_ele
                    else:
                        new_ele = 'null'
                    new_line.append(new_ele)
                report.append(new_line)
            return report
        else:
            print('报告读取失败')
            return report

# 超载报告数据入库
    def __get_ovld_sql(self,ovld_report):
        for data in ovld_report:
            # print(data)
            ovld_sql = ("""insert into bstest.overload_report (alarm_uuid,train_order,veh_num,
                guide_end,report_time,week_day,veh_type,veh_label,veh_plat,velocity,
                bogie1_cred,bogie2_cred,wgt,max_wgt,self_wgt,ovld_wgt,ovld_pct,
                ovld_alarm_lv,etl_source) values ("""
                + "'" + data[0] + "'" +","                              #alarm_uuid
                + "'" + data[1] + "'" +","                              #train_order
                + data[3] + ","                                         #veh_num
                + "'" + data[4] + "'" + ","                             #guide_end
                + "'" + data[5].split('|')[1] + "'" + ","               #report_time
                + "'" + data[5].split('|')[0] + "'" + ","               #week_day
                + "'" + data[6] + "'" + ","                             #veh_type
                + "'" + data[7] + "'" + ","                             #veh_label
                + "'" + data[8] + "'" + ","                             #veh_plat
                + data[9] + ","                                         #velocity
                + data[10] + ","                                         #bogie1_cred
                + data[11] + ","                                        #bogie2_cred
                + data[12] + ","                                        #wgt
                + data[13] + ","                                        #max_wgt
                + data[14] + ","                                        #self_wgt
                + data[15] + ","                                        #ovld_wgt
                + data[16] + ","                                        #ovld_pct
                + "'" + data[17] + "'" + ","                            #ovld_alarm_lv
                + "'" + data[2] + "'"                                   #etl_source
                + ");"
            )
            self.db.execute_sql(ovld_sql)
            LocoAlarmSpider.ovld_cnt += 1
            print('正在插入第[' + str(LocoAlarmSpider.ovld_cnt) + ']条车辆超载数据...')

# 偏载报告数据入库
    def __get_imba_sql(self,imba_report):
        for data in imba_report:
            imba_sql = ("""insert into bstest.imbalance_report (alarm_uuid,train_order,veh_num,
                guide_end,report_time,week_day,veh_type,veh_label,veh_plat,
                bogie1_cred,bogie2_cred,velocity,wgt,bogie1_wgt,bogie2_wgt,
                axis1_lwgt,axis1_rwgt,axis1_diff,
                axis2_lwgt,axis2_rwgt,axis2_diff,
                axis3_lwgt,axis3_rwgt,axis3_diff,
                axis4_lwgt,axis4_rwgt,axis4_diff,
                axis5_lwgt,axis5_rwgt,axis5_diff,
                axis6_lwgt,axis6_rwgt,axis6_diff,
                axis7_lwgt,axis7_rwgt,axis7_diff,
                axis8_lwgt,axis8_rwgt,axis8_diff,
                bogie1_wgt_diff,bogie2_wgt_diff,bogie1_imba_offset,bogie2_imba_offset,
                imba_alarm_lv,bogie1_imba_alarm,bogie2_imba_alarm,etl_source) 
                values ("""
                + "'" + data[0] + "'" +","                      #alarm_uuid
                + "'" + data[1] + "'" + ","                     #train_order
                + data[3] + ","                                 #veh_num
                + "'" + data[4] + "'" + ","                     #guide_end
                + "'" + data[5].split('|')[1] + "'" + ","       #report_time
                + "'" + data[5].split('|')[0] + "'" + ","       #week_day
                + "'" + data[6] + "'" + ","                     #veh_type
                + "'" + data[7] + "'" + ","                     #veh_label
                + "'" + data[8] + "'" + ","                     #veh_plat
                + data[9] + ","                                 #bogie1_cred
                + data[10] + ","                                 #bogie2_cred
                + data[11] + ","                                #velocity
                + data[12] + ","                                #wgt
                + data[13] + ","                                #bogie1_wgt
                + data[14] + ","                                #bogie2_wgt
                + data[15] + ","                                #axis1_lwgt
                + data[16] + ","                                #axis1_rwgt
                + data[17] + ","                                #axis1_diff
                + data[18] + ","                                #axis2_lwgt
                + data[19] + ","                                #axis2_rwgt
                + data[20] + ","                                #axis2_diff
                + data[21] + ","                                #axis3_lwgt
                + data[22] + ","                                #axis3_rwgt
                + data[23] + ","                                #axis3_diff
                + data[24] + ","                                #axis4_lwgt
                + data[25] + ","                                #axis4_rwgt
                + data[26] + ","                                #axis4_diff
                + data[27] + ","                                #axis5_lwgt
                + data[28] + ","                                #axis5_rwgt
                + data[29] + ","                                #axis5_diff
                + data[30] + ","                                #axis6_lwgt
                + data[31] + ","                                #axis6_rwgt
                + data[32] + ","                                #axis6_diff
                + data[33] + ","                                #axis7_lwgt
                + data[34] + ","                                #axis7_rwgt
                + data[35] + ","                                #axis7_diff
                + data[36] + ","                                #axis8_lwgt
                + data[37] + ","                                #axis8_rwgt
                + data[38] + ","                                #axis8_diff
                + data[39] + ","                                #bogie1_wgt_diff
                + data[40] + ","                                #bogie2_wgt_diff
                + data[41] + ","                                #bogie1_imba_offset
                + data[42] + ","                                #bogie2_imba_offset
                + "'" + data[43] + "'" + ","                    #imba_alarm_lv
                + "'" + data[44] + "'" + ","                    #bogie1_imba_alarm
                + "'" + data[45] + "'" + ","                    #bogie2_imba_alarm
                + "'" + data[2] + "'"                           #etl_source
                + ");"
            )
            self.db.execute_sql(imba_sql)
            LocoAlarmSpider.imba_cnt += 1
            print('正在插入第[' + str(LocoAlarmSpider.imba_cnt) + ']条车辆偏载数据...')

# 机车报警数据入库
    def __get_loco_alarm_sql(self,anchor):
        # for anchor in anchors:
        #     if anchor['warn_confirm'] == '已确认':
        alarm_sql = ("""insert into bstest.loco_alarm (uuid,trainDateTime,location,track,timeZone,
        train_order,alarm_time,station,track_num,direction,first_loco,velocity,total_loco,
        total_car,total_axis,total_weight,max_vertical_force,max_dynamic_load,
        max_ratio,max_transverse_stress,max_instability_index,train_warn,
        warn_confirm,overload_url,imbalance_url,etl_source) values ("""
        + "'" + anchor['uuid'] + "'" +","
        + "'" + anchor['trainDateTime'] + "'" + ","
        + "'" + anchor['location'] + "'" + ","
        + "'" + anchor['track'] + "'" + ","
        + "'" + anchor['timeZone'] + "'" + ","
        + "'" + anchor['train_order'] + "'" + ","
        + "'" + anchor['alarm_time'] + "'" + ","
        + "'" + anchor['station'] + "'" + ","
        + "'" + anchor['track_num'] + "'" + ","
        + "'" + anchor['direction'] + "'" + ","
        + "'" + anchor['first_loco'] + "'" + ","
        + anchor['velocity'] + ","
        + anchor['total_loco'] + ","
        + anchor['total_car'] + ","
        + anchor['total_axis'] + ","
        + anchor['total_weight'] + ","
        + anchor['max_vertical_force'] + ","
        + anchor['max_dynamic_load'] + ","
        + anchor['max_ratio'] + ","
        + anchor['max_transverse_stress'] + ","
        + anchor['max_instability_index'] + ","
        + "'" + anchor['train_warn'] + "'" + ","
        + "'" + anchor['warn_confirm'] + "'" + ","
        + "'" + anchor['overload_url'] + "'" + ","
        + "'" + anchor['imbalance_url'] + "'" + ","
        + "'" + self.rc.get_url('loco_url') + "'"
        + ");")
        # print(alarm_sql)
        self.db.execute_sql(alarm_sql)
        LocoAlarmSpider.loco_alarm_cnt += 1
        print('正在插入第[' + str(LocoAlarmSpider.loco_alarm_cnt) + ']条已确认的机车告警数据...')

    def go(self,loco_alarm_url):
        try:
            htmls = self.__fetch_content(loco_alarm_url)
            raw_anchors = self.__analysis(htmls)
            anchors = self.__refine_alarm(raw_anchors)
            self.db.conn_db()
            for anchor in anchors:
            #     if anchor['warn_confirm'] == '已确认':
            #         print('这一步运行了么')
                self.__get_loco_alarm_sql(anchor)
                ovld_report = self.__fetch_report(anchor['overload_url'],anchor['uuid'],anchor['train_order'])
                imba_report = self.__fetch_report(anchor['imbalance_url'],anchor['uuid'],anchor['train_order'])
                self.__get_ovld_sql(ovld_report)
                self.__get_imba_sql(imba_report)
            self.db.commit_sql()
            print('共插入[' + str(LocoAlarmSpider.loco_alarm_cnt) + ']条已确认的机车告警数据')
            print('共插入[' + str(LocoAlarmSpider.ovld_cnt) + ']条车辆超载报告数据')
            print('共插入[' + str(LocoAlarmSpider.imba_cnt) + ']条车辆偏载报告数据')
        finally:
            self.db.close_conn()
