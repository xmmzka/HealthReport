# 15 Mar 2022 | 8:05 PM
# main

import requests
# 请求地址
url = 'http://api.njust.edu.cn:80/appHealthReport/healthReport/search'

# 请求头
headers = {
    'Host': 'api.njust.edu.cn',
    'Connection': 'keep-alive',
    'Content-Length': '197',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': ('Mozilla/5.0 (Linux; Android 11; M2007J1SC Build/RKQ1.200826.002; wv) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Version/4.0 Chrome/86.0.4240.99 XWEB/3193 MMWEBSDK/20220204 Mobile Safari/537.36 '
                   'MMWEBID/6348 MicroMessenger/8.0.20.2100(0x2800143D) '
                   'Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64'),
    'Content-Type': 'application/json',
    'Origin': 'http://api.njust.edu.cn',
    'X-Requested-With': 'com.tencent.mm',
    'Referer': 'http://api.njust.edu.cn/healthReport/healthReport.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '****'
}

# 请求体
data = {
    'account': '*',
    'userName': '*',
    'userType': '1',
    'deptName': '*',
    'deptId': '102',
    'grade': '2020',
    'className': '*',
    'timeNum': 2,
    'temperature': 1,
    'isCough': 0
}

# body = json.dumps(data).encode('utf-8')
# http = urllib3.PoolManager()
# r = http.request('POST', url, fields = body, headers = headers)

# url = url + '?' + urlencode(data)
# http = urllib3.PoolManager()
# r = http.request('POST', url, headers = headers)
# print(r.status)
# print(r.headers)
# print(r.data)

response = requests.post(url, headers = headers, json = data)
print('[status]===================================')
print(response.status_code)
print('[headers]==================================')
print(response.headers)
print('[json]=====================================')
print(response.json())
