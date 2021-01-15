import requests
import redis
import pymysql
import time
import json

#将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp

class test_rule:
    def __init__(self,pool_id,startTime=1607085000,endTime=1608277706,ratio=83):
        # 1.连接
        self.conn = pymysql.connect(host='public-cpwg-db334.idcyz.hb1.kwaidc.com', port=15186, user='test_rw', password='54rltyi5BCdcm06wu22A0brvvzU5uDgB', db='test', charset='utf8')
        print(self.conn)
        self.redis_conn = redis.StrictRedis(host='10.75.61.228', port=6379, db=8,decode_responses=True)
        print(self.redis_conn)
        # 2.创建游标
        self.cursor = self.conn.cursor()
        self.startTime=startTime
        self.endTime=endTime
        self.ratio=ratio
        self.pool_id=pool_id
        self.db_name = "draw_result_"+pool_id
        self.db_res = "draw_result_res_"+pool_id
        self.transfer_data()

    def create(self,sql,db):
        try:
            res=self.cursor.execute(sql)
        except:
            sql_drop = "drop table %s;"%(db)
            self.cursor.execute(sql_drop)
            res=self.cursor.execute(sql)
        print(res)

    def transfer_time(self,curtimestamp):
        # lengthTem = (int)(curtimestamp) - self.startTime
        # timeEndStamp = self.endTime + lengthTem*self.ratio
        try:
            t = float(curtimestamp)
        except:
            return
        t = time.localtime(t)
        t = time.strftime("%Y-%m-%d %H:%M:%S",t)
        return t

    def transfer_data(self):
        sql1="create table %s (time char(10),draw_time datetime,uid varchar(8),pid varchar(6));"%(self.db_name)
        sql2="create table %s (rule varchar(200),uid varchar(8),real_cnt int);"%(self.db_res)
        self.create(sql1,self.db_name)
        self.create(sql2,self.db_res)
        drawres_uids = self.redis_conn.lrange(self.db_name, 0, -1)
        for drawres_uid in drawres_uids:
            pid=drawres_uid.split('____')           
            tm = self.transfer_time(pid[0])       
            if tm is not None and len(pid)==3:            
                sql = "insert into %s values('%s','%s','%s','%s');" %(self.db_name,pid[0],tm, pid[1],pid[2])
                # print(sql)
                # 3.执行sql语句
                res=self.cursor.execute(sql)
                # print(pid)
        self.conn.commit()

    def sql_exe(self,sql):
        self.cursor.execute(sql)

    def test_limit(self,rule):
        plist=rule["prizeTypes"]
        limitCount=rule["limitCount"]
        sql="select uid,count(uid) from %s where pid='%s'"%(self.db_name,plist[0])
        for i in range(1,len(plist)):
            sql+=" or pid='%s'"%(plist[i])
        sql+=' group by uid;'
        print(sql)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        for r in res:
            # print(r[1])
            if r[1]>limitCount: 
                s=str(rule)
                s=s.replace("'"," ")
                print(s)
                sql = "insert into %s values('%s','%s','%s');" %(self.db_res,s,r[0],r[1])
                print(sql)
                self.cursor.execute(sql)
        self.conn.commit()       

    def test_total(self,pid,total_cnt):
        sql="select count(pid) from %s where pid='%s';"%(self.db_name,pid)
        res=self.sql_exe(sql=sql)
        if res==total_cnt: 
            return '1',res
        else: 
            return '0',res

    def test_date(self,pid,date_rules):
        print(pid)
        print(date_rules)
        total=0
        num=int(date_rules['times'])*(date_rules['count'])
        days=date_rules['step']
        start=date_to_timestamp(date_rules['startDateStr']+' '+date_rules['startTimeStr'])
        end=date_to_timestamp(date_rules['endDateStr']+' '+date_rules['endTimeStr'])
        sql="select time from %s where pid='%s'"%(self.db_name,pid)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        # print(res)
        for r in res:
            if float(r[0])>=float(start) and float(r[0])<=float(end): 
                total=total+1
        if total>num:
            sql = "insert into %s values('%s','%s','%s');" %(self.db_res,date_rules,str(num),str(total))
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()

    def __del__(self):
        # 关闭连接，游标和连接都要关闭
        self.cursor.close()
        self.conn.close()

def draw_result():
    pool_id = "226"
    t=test_rule(pool_id)
    with open('rule.json','rb') as f:
        rules = json.load(f)
    print(len(rules))
    limit_rules=rules['prizePoolCreateDTO']['constraintStrategyListExtData']['prizeTypesToLimitCountPairs']
    for rule in limit_rules:
        print(rule)
        t.test_limit(rule)
    prizeCreateDTOs=rules['prizeCreateDTOs']
    for item in prizeCreateDTOs:
        pid=item['type']
        dateToCountDTOs=item['visibleFactorToCountExtData']['dateToCountDTOs']
        for date_rules in dateToCountDTOs:
            t.test_date(pid,date_rules)
    print('执行完毕')


# #查询当前key的类型
# def getTypeByKey(key):
#         ret = redis_conn.type(key)
#         return ret
draw_result()