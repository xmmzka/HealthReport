# main_v2.0.0
# Friday, March 18, 2022 4:31 PM
# com.circute
import requests
import time
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
        'Cookie': 'lxwxuserid=Z+zfE7RYJ0/ak91q27yAWA=='
    }
    body = {}
    defaultaccount = '9201020H0425'  # 预设的账户(学号)

    times = 5  # 尝试获取JSESSIONID的次数
    for times_var in range(0, times):
        try:
            response = requests.post(
                url, headers=headers, json=body, timeout=10)
            if response.status_code == 200:
                try:
                    account = response.json()['data']['account']
                    print('[', time.time(), '] ',
                          'The queried account is: ', account, sep='')
                    if account == defaultaccount:
                        print('    ==> OK')
                    else:
                        print('    ==> ERROR: Account mismatch')
                        return 'acontmismatch'
                except:
                    print('[', time.time(), '] ',
                          'Failed to get return account', sep='')
                    print('    ==> Current number of requests:', times_var + 1)
                    continue
                try:
                    jsonid = response.headers['Set-Cookie'].split(';')[
                        0].split('=')[-1]
                    print('[', time.time(), '] ',
                          'The JSESSIONID of this request has been obtained:', sep='')
                    print('    ==> JSESSIONID =', jsonid)
                    return jsonid
                except:
                    print('[', time.time(
                    ), '] There was an error in getting JSESSIONID from the returned headers.')
                    print('    ==> Current number of requests:', times_var + 1)
            else:
                print('[', time.time(), '] ',
                      'There is a problem with the returned status code:', sep='')
                print('    ==> status code:', response.status_code)
                print('    ==> Current number of requests:', times_var + 1)
        except:
            print('[', time.time(), '] ',
                  'An exception occurred while calling the post method:', sep='')
            print('    ==> Current number of requests:', times_var + 1)
    return 'error'


def postinfo(jsonid, num):
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
    times = 5
    for times_var in range(0, times):
        try:
            response = requests.post(
                url, headers=headers, json=body, timeout=10)
            if response.status_code == 200:
                try:
                    if response.json()['status'] == 0:
                        if response.json()['data']['timeNum'] == num - 1:
                            print('[', time.time(), '] ',
                                  'Completed successfully!', sep='')
                            return True
                        else:
                            print('[', time.time(), '] ', 'Failed', sep='')
                            print('    ==> Current number of requests:',
                                  times_var + 1)
                    else:
                        print('[', time.time(), '] message: ',
                              response.json()['message'], sep='')
                        print('    ==> status:', response.json()['status'])
                        return False
                except:
                    pass
            else:
                print('[', time.time(), '] ',
                      'There is a problem with the returned status code:', sep='')
                print('    ==> status code:', response.status_code)
                print('    ==> Current number of requests:', times_var + 1)
        except:
            print('[', time.time(), '] ',
                  'An exception occurred while calling the post method:', sep='')
            print('    ==> Current number of requests:', times_var + 1)
    return False

    # for times_var in (0, times):
    #     response = requests.post(url, headers=headers, json=body, timeout=10)
    #     if response.status_code == 200:
    #         if response.json()['status'] == 0:
    #             if response.json()['data']['timeNum'] == num + 1:
    #                 print('[', time.time(), '] ', 'Completed successfully!', sep='')
    #                 return True
    #             else:
    #                 print('[', time.time(), '] ', 'Failed', sep='')
    #                 print('    ==> Current number of requests:', times_var + 1)
    #         else:
    #             print('[', time.time(), '] ', response.json()['message'], sep='')
    #             print('    ==> status:', response.json()['status'])
    #             return False
    #     else:
    #         print('[', time.time(), '] ', 'There is a problem with the returned status code:', sep='')
    #         print('    ==> status code:', response.status_code)
    #         print('    ==> Current number of requests:', times_var + 1)
    #     time.sleep(5)
    # return False


def notice(text):
    url = 'https://maker.ifttt.com/trigger/notice_phone/with/key/cXXJcQO4NOmhYCltdou5Wj'
    headers = {'Content-Type': 'application/json'}
    body = {'value1': text}
    try:
        requests.post(url, headers=headers, json=body)
    except:
        pass


def main(num):
    jsonid = getjsonid()
    if jsonid == 'acontmismatch':
        pass
    elif jsonid == 'error':
        pass
    else:
        if postinfo(jsonid, num):
            pass
        else:
            pass

# def main(num):
#     jsonid = getjsonid()
#     if jsonid == 'acontmismatch':
#         notice('在查询JSESSIONID时,账户名不匹配,本次自动提交失败,请手动填写,并查看服务器日志.')
#     elif jsonid == 'error':
#         notice('请求错误,本次自动提交失败,请手动填写,并查看服务器日志.')
#     else:
#         if postinfo(jsonid, num):
#             pass
#         else:
#             notice('发送数据时出错,请手动填写,并查看服务器日志.')


schedule.every().day.at("22:00").do(main, 0)
schedule.every().day.at("04:00").do(main, 1)
schedule.every().day.at("10:00").do(main, 2)
while True:
    schedule.run_pending()
    time.sleep(2)
