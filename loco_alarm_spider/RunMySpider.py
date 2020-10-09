from loco_alarm_spider.LocoAlarmSpider import LocoAlarmSpider
from loco_alarm_spider.GetCookies import GetCookies
import time

if __name__ == "__main__":
    ck = GetCookies()
    try:
        start_time = time.time()
        ck.update_cookies()
        # time.sleep(1)
        las = LocoAlarmSpider()
        loco_url = las.loco_url
        las.go(loco_url)
        end_time = time.time()
        dtime = end_time - start_time
        print("程序运行时间：%s s" % int(dtime))
    finally:
        ck.driver_quit()
