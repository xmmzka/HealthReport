# Wednesday, March 16, 2022 2:18 PM
# com.ciucute
# main

# The information in the asterisk section needs to be filled in

import requests
import time
import schedule


def getjsonid():
    "Get the JSESSIONID of the request"
    url = 'http://api.njust.edu.cn:80/appHealthReport/healthReport/rights'

    headers = {
        'Host': 'api.njust.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '2',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': ('Mozilla/5***************KQ1.200826.002; wv) '
                       'AppleWeb************ersion/4.0 Chrome/86.0.4240.99 '
                       'XWEB/3193 ******************37.36 MMWEBID/6348 '
                       'MicroMessenger******************* Process/toolsmp '
                       'WeChat/arm64********************ge/zh_CN ABI/arm64'),
        'Content-Type': 'application/json',
        'Origin': 'http://api.njust.edu.cn',
        'X-Requested-With': 'com.tencent.mm',
        'Referer': 'http://api.njust.edu.cn/healthReport/healthReport.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'lxwxuserid=******************'
    }

    body = {}

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        # Extract JSESSIONID
        jsonid = response.headers['Set-Cookie'].split(';')[0].split('=')[-1]
        print('[', time.time(), ']', ' OK', sep='')
        print('    status code ==> 200 | JSEEEIONID(GET) =', jsonid)
        print('=======================================================================>>>')
        print(response.json())
        print('=======================================================================>>>')
        return jsonid
    else:
        print('[', time.time(), ']', ' !!!ERROR', sep='')
        print('    status code ==>', response.status_code)
        print('=======================================================================>>>')
        print(response.json())
        return '!'


def post(jessionid, timenum):
    "send data"
    if jessionid == '!':
        return False
    else:
        url = 'http://api.njust.edu.cn:80/appHealthReport/healthReport'
        cookie = 'lxwxuserid=***********************; wxAccount=********************; JSESSIONID=' + jessionid
        headers = {
            'Host': 'api.njust.edu.cn',
            'Connection': 'keep-alive',
            'Content-Length': '197',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': ('Mozilla/5.0 (Lin*****************00826.002; wv) '
                           'AppleWebKi***************************on/4.0 Chrome/86.0.4240.99 '
                           'XWEB/3193 MM*************************************MMWEBID/6348 '
                           'MicroMesse***************************) Process/toolsmp WeChat/arm64 '
                           'Weixin N********************** ABI/arm64'),
            'Content-Type': 'application/json',
            'Origin': 'http://api.njust.edu.cn',
            'X-Requested-With': 'com.tencent.mm',
            'Referer': 'http://api.njust.edu.cn/healthReport/healthReport.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': cookie
        }
        body = {
            'account': '9201020H04**',
            'userName': '****',                 # name
            'userType': '1',                    # default '1'
            'deptName': '环境与生物工程学院',
            'deptId': '102',
            'grade': '2020',
            'className': '9201020H04',
            'timeNum': timenum,
            'temperature': 1,
            'isCough': 0
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            jsonid = response.headers['Set-Cookie'].split(';')[0].split('=')[-1]
            print('[', time.time(), ']', ' OK', sep='')
            print('    status code ==> 200 | JSEEEIONID =', jsonid)
            print('=======================================================================>>>')
            print(response.headers)
            print(response.json())
            print('=======================================================================>>>')
            return True
        else:
            print(response.status_code)
            print('=======================================================================>>>')
            print(response.headers)
            print(response.json())
            print('=======================================================================>>>')
            return False


def work(num):
    "Call the function that sends the request. Num is the number of reports"
    print('[', time.time(), '] ', 'start...', sep='')
    i = 5
    while i > 0:
        if post(getjsonid(), num):
            print('[', time.time(), '] ', 'OK', sep='')
            break
        else:
            print('[', time.time(), '] ', 'Error', sep='')  # Try five times
            i = i - 1
            print('    times ==>', i)
    # !!!warnimg


def timemanager():
    "Master of time management "
    # Reporting time: 6:00/12:00/18:00
    # My Linux server time is 8 hours slower than Shanghai time. (UTC)
    schedule.every().day.at("22:00").do(work, 0)
    schedule.every().day.at("04:00").do(work, 1)
    schedule.every().day.at("10:00").do(work, 2)
    # test:
    # schedule.every().day.at("10:35").do(work, 2)
    while True:
        schedule.run_pending()
        time.sleep(20)  # Test time every 20 seconds


# post(getjsonid(), 4)
timemanager()
