from loco_alarm_spider.ReadConfig import ReadConfig
import pymysql

class HandleDB:
    def __init__(self):
        self.rc = ReadConfig()

    def conn_db(self):
        try:
            host = self.rc.get_dbinfo('host')
            port = int(self.rc.get_dbinfo('port'))
            user = self.rc.get_dbinfo('user')
            password = self.rc.get_dbinfo('password')
            db = self.rc.get_dbinfo('db')
            charset = self.rc.get_dbinfo('charset')
            self.conn = pymysql.connect(host=host,port=port,user=user,password=password,db=db,charset=charset)
            self.cur = self.conn.cursor()
        except:
            print('数据库连接失败！')
        else:
            print('数据库连接成功！')

    def execute_sql(self,sql):
        # self.conn_db()
        self.cur.execute(sql)
        # self.conn.commit()


    def close_conn(self):
        self.cur.close()
        self.conn.close()
        print('数据库已关闭连接')

    def query(self,sql):
        # self.conn_db()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def commit_sql(self):
        self.conn.commit()


# if __name__ == '__main__':
#     db = HandleDB()
#     db.conn_db()