from JdSpider.MySpider import MySpider
import time

if __name__ == "__main__":
        start_time = time.time()
        # time.sleep(1)
        ms = MySpider()
        ms.go()
        end_time = time.time()
        dtime = end_time - start_time
        print("程序运行时间：%s s" % int(dtime))

