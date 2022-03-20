import requests
import time

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
        'Cookie': 'lxwxuserid=Z+zfE7RYJ0/ak91q27yAWA=='
    }

    body = {}

    for times in range(0, 5):
        try:
            response = requests.post(url, headers=headers, json=body)
        except:
            continue
        if response.status_code == 200:
            try:
                jsonid = response.headers['Set-Cookie'].split(';')[0].split('=')[-1]
                print('[', time.time(), '] The JSESSIONID of this request has been obtained: ', jsonid, sep='')
                return jsonid
            except:
                print('[', time.time(), '] ERROR: ', response.headers)
    return 'ERROR'

def postinfo(num, jsonid):
    url = 'http://api.njust.edu.cn:80/appHealthReport/healthReport'
    cookie = 'lxwxuserid=Z+zfE7RYJ0/ak91q27yAWA==; wxAccount=OTIwMTAyMEgwNDI1; JSESSIONID=' + jsonid
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
        'account': '9201020H0425',
        'userName': '孙逸',
        'userType': '1',
        'deptName': '环境与生物工程学院',
        'deptId': '102',
        'grade': '2020',
        'className': '9201020H04',
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
                if response.json()['status'] == 0 & response.json()['message'] == 'success':
                    if response.json()['data']['timeNum'] == (str)(num + 1):
                        return True
            except:
                pass
            print(response.headers)
            print(response.json())
            print('times:', times + 1)
    return False

def main(num):
    jsonid = getjsonid()
    if jsonid == 'ERROR':
        return False
    else:
        if postinfo(num, jsonid):
            print('success')
        else:
            print('FAILED')

main(2)