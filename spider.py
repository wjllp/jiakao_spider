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
    
    dataurl = 'http://hb.122.gov.cn/m/examplan/getExamPlan'
    detailurl = 'http://hb.122.gov.cn/m/examplan/getExamPlanDetail'
    data = {
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
        resp = session.post(dataurl,data=data)
        soup = BeautifulSoup(resp.text, 'html.parser')
    except:
        print('出问题了')
    myjson = json.loads(str(soup))
    if len(myjson) == 3:
        for i in range(len(myjson['data']['content'])):
            kcmc = myjson['data']['content'][i]['kcmc']    #考场名称
            if kc in kcmc:
                data['ksdd'] = myjson['data']['content'][i]['kcdddh']    #给post数据赋新值
                try:
                    resp = session.post(detailurl,data=data)
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    detailjson = json.loads(str(soup))
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
                    if (int(sqrs) != 0):
                        print (kcmc,ksrq,sqrs)
                        if mydao.is_new(kcmc,ksrq,kskm) == True:
                            print ("是最新的")
                            text = text + kcmc + ' ' + ksrq + ' ' + detailjson['data'][j]['kscx'] + ' 科目'+str(kskm)+'\n'
                            flag = 1
                            mydao.insert_result(kcmc,ksrq,kskm)
                            print (kcmc,ksrq,sqrs)
                print(text)
                if flag == 1:
                    emails = mydao.select_user_mail(kskm,kc)
                    for email in emails:
                        print (email)
                        sendmail(email['email'],text,'有新的科目'+str(kskm)+'考试安排出来了',' ')
                        
if __name__ == '__main__':
    infs = mydao.select_distinct_info()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for inf in infs:
        spider(inf['kskm'],inf['kcmc'])

