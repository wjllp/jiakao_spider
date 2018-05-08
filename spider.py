#code:utf-8
from dao import mydao
from sendmail import *
import time
import requests
from bs4 import BeautifulSoup
import json
session = requests.session()
def spider(kskm,kc):
    currenttime = time.localtime()
    startTime = time.strftime("%Y-%m-%d", currenttime)
    year = time.strftime("%Y",currenttime)
    month = time.strftime("%m",currenttime)
    day = time.strftime("%d",currenttime)
    
    month = str(int(month) + 2)
    endTime = year + '-' + month + '-' + day
    
    dataurl = 'http://hb.122.gov.cn/m/examplan/getExamPlan'       #考场信息概览
    detailurl = 'http://hb.122.gov.cn/m/examplan/getExamPlanDetail'     #考场详细信息
    data = {            #请求体
        'endTime':endTime,
        'fzjg':'鄂G',
        'kscx':'C1',
        'ksdd':'',
        'kskm':kskm,         #考试科目
        'page':0,
        'startTime':startTime,
        'zt':0
    }
    try:
        resp = session.post(dataurl,data=data)  #post提交数据
        soup = BeautifulSoup(resp.text, 'html.parser')    #bs解析html
    except:
        print('出问题了')
    myjson = json.loads(str(soup))     #转化为json
    if len(myjson) == 3:
        for i in range(len(myjson['data']['content'])):
            kcmc = myjson['data']['content'][i]['kcmc']    #提取考场名称
            if kc in kcmc:
                data['ksdd'] = myjson['data']['content'][i]['kcdddh']    #获取考场详细信息后给post数据重新赋值
                try:
                    resp = session.post(detailurl,data=data)    #重新提交数据
                    soup = BeautifulSoup(resp.text, 'html.parser')    #解析html
                    detailjson = json.loads(str(soup))        #转化为json
                except:
                    print('Detail出问题了')
                text = ''
                kcmc = ''
                ksrq = ''
                flag = 0
                for j in range(len(detailjson['data'])):
                    kcmc = detailjson['data'][j]['kcmc']  #考场名称
                    ksrq = detailjson['data'][j]['ksrq']  #考试日期
                    sqrs = detailjson['data'][j]['sqrs']  #预约人数
                    if (int(sqrs) != 0):      #当预约人数大于0则说明指标已出来
                        if mydao.is_new(kcmc,ksrq,kskm) == True:      #判断是否是新出来的指标
                            text = text + kcmc + ' ' + ksrq + ' ' + detailjson['data'][j]['kscx'] + ' 科目'+str(kskm)+'\n'
                            flag = 1
                            mydao.insert_result(kcmc,ksrq,kskm)    #插入数据库
                if flag == 1:
                    emails = mydao.select_user_mail(kskm,kc)   #查询注册了这场考试的用户
                    for email in emails:
                        sendmail(email['email'],text,'有新的科目'+str(kskm)+'考试安排出来了',' ')  #发送邮件通知用户
                        
if __name__ == '__main__':
    infs = mydao.select_distinct_info()   #查询总共有哪些考场
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for inf in infs:
        spider(inf['kskm'],inf['kcmc'])

