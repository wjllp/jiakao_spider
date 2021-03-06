#coding:utf-8
import datetime
import pymysql.cursors
connection = pymysql.connect(host='127.0.0.1',
                             port=3360,
                             user='root',
                             password='root',
                             db='jiakao',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
def is_new(kcmc,ksrq,kskm):
    sql = "select * from result where kcmc = '%s' and ksrq = '%s' and kskm = %d"
    data = (kcmc,ksrq,kskm)
    cursor.execute(sql%data)
    if(cursor.rowcount) == 0:         #若为0则表示是最新的
        return True
    else:
        return False

def select_user():
    sql = "select * from user"
    cursor.execute(sql)
    connection.commit()
    return cursor.fetchall()

def insert_result(kcmc,ksrq,kskm):
    sql = "insert into result(kskm,kcmc,ksrq) values ('%d','%s','%s')"
    data = (kskm,kcmc,ksrq)
    cursor.execute(sql%data)
    connection.commit()
    print('添加结果成功！')

def insert_user(email,kcmc,kskm):
    sql = "insert into user(email,kcmc,kskm) values('%s','%s','%d')"
    data = (email,kcmc,kskm)
    cursor.execute(sql%data)
    connection.commit()
    print('添加用户成功')

def select_distinct_info():
    sql = "select distinct kskm,kcmc from user"
    cursor.execute(sql)
    connection.commit()
    return cursor.fetchall()

def select_user_mail(kskm,kcmc):
    sql = "select email from user where kskm = '%s' and kcmc = '%s'"
    data = (kskm,kcmc)
    cursor.execute(sql%data)
    connection.commit()
    return cursor.fetchall()
