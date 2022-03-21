# main v2.1.0
# Monday, March 21, 2022 1:32 PM

import time
import requests
import schedule


def getjsonid():
    url = 'http://api.njust.edu.cn:80/appHealthReport/healthReport/rights'
    headers = {
        'Host': 'api.njust.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '2',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 11; M2007J1SC Build/RKQ1.200826.002; wv) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 '
                       'XWEB/3193 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6348 '
                       'MicroMessenger/8.0.20.2100(0x2800143D) Process/toolsmp '
                       'WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64'),
        'Content-Type': 'application/json',
        'Origin': 'http://api.njust.edu.cn',
        'X-Requested-With': 'com.tencent.mm',
        'Referer': 'http://api.njust.edu.cn/healthReport/healthReport.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'lxwxuserid=######################'
    }
    body = {}
    for times in range(0, 5):
        print('[', time.time(), '] ', 'times: ', times, sep='')
        try:
            response = requests.post(url, headers=headers, json=body, timeout=5)
        except:
            continue
        if response.status_code == 200:
            try:
                jsonid = response.headers['Set-Cookie'].split(';')[0].split('=')[-1]
                print('[', time.time(), '] The JSESSIONID of this request has been obtained: ', jsonid, sep='')
                return jsonid
            except:
                print('[', time.time(), '] ERROR')
    return 'ERROR'


def postinfo(num, jsonid):
    url = 'http://api.njust.edu.cn:80/appHealthReport/healthReport'
    cookie = 'lxwxuserid=#####################; wxAccount=#################; JSESSIONID=' + jsonid
    headers = {
        'Host': 'api.njust.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '197',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 11; M2007J1SC Build/RKQ1.200826.002; wv) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 '
                       'XWEB/3193 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/6348 '
                       'MicroMessenger/8.0.20.2100(0x2800143D) Process/toolsmp WeChat/arm64 '
                       'Weixin NetType/WIFI Language/zh_CN ABI/arm64'),
        'Content-Type': 'application/json',
        'Origin': 'http://api.njust.edu.cn',
        'X-Requested-With': 'com.tencent.mm',
        'Referer': 'http://api.njust.edu.cn/healthReport/healthReport.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': cookie
    }
    body = {
        'account': '9201020H04##',
        'userName': '###',
        'userType': '1',
        'deptName': '环境与生物工程学院',
        'deptId': '102',
        'grade': '2020',
        'className': '9201022701',
        'timeNum': num,
        'temperature': 1,
        'isCough': 0
    }
    for times in range(0, 5):
        try:
            response = requests.post(url, headers=headers, json=body, timeout=5)
        except:
            continue
        if response.status_code == 200:
            try:
                if response.json()['status'] == 0 and response.json()['message'] == 'success':
                    if response.json()['data']['timeNum'] == (str)(num + 1):
                        return True
            except:
                pass
            try:
                print('[', time.time(), '] message: ', response.json()['message'], '(times: ', times + 1, ')', sep='')
                print('    ==> json:', response.json())
            except:
                print('[', time.time(), '] Parsing failed', sep='')
    return False


def main(num):
    jsonid = getjsonid()
    if jsonid == 'ERROR':
        notice('获取JSESSIONID失败,请查看服务器日志!', '在getjsonid()函数调用过程中出现错误,获取JSESSIONID失败,无法向目标url返回数据.')
    else:
        if postinfo(num, jsonid):
            print('success')
        else:
            notice('数据上传失败,请查看服务器日志!', '调用postinfo()函数时出现错误,返回值False,数据上传失败.')


def notice(summary, message):
    url = 'http://wxpusher.zjiecode.com/api/send/message'
    body = {
        'appToken': 'AT_################################',
        'content': message,
        'summary': summary,
        'contentType': 1,
        'uids': ['UID_###########################']
    }
    try:
        response = requests.post(url, json=body)
        print(response.json())
    except:
        print('[', time.time(), '] ', 'Failed to send notification.', sep='')


# main:
# Reporting time: 6:00/12:00/18:00
# Linux server time is 8 hours slower than Shanghai time. (UTC)
schedule.every().day.at("22:00:05").do(main, 0)
schedule.every().day.at("04:00:05").do(main, 1)
schedule.every().day.at("10:00:05").do(main, 2)

while True:
    schedule.run_pending()
    time.sleep(1)
