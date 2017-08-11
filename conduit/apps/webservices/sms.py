from rest_framework.exceptions import ValidationError
import http, json
from urllib import request, parse, error

yunpianApiKey = "257b42a0e9a6d2f58fc9dcb176fa24da"
urlSendSmsYunpian = "https://sms.yunpian.com/v2/sms/single_send.json"

IoTAuthorization = 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJzaGJramQiLCJleHAiOjE1MDI0NDY3MDF9.kX4vTBM3AnfJ510uoa7En9a-9gT7nF_qyWqzGtHIFf4'
urlSendSmsIoT = 'http://120.26.213.169/api/sms/'


def sms_send_normal(content, receiver):

    dataSendSms = "apikey=" + yunpianApiKey + "&mobile=" + receiver + "&text=" + content
    data = dataSendSms.encode('utf-8')
    headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    req = request.Request(urlSendSmsYunpian, headers=headers)
    try:
        response = request.urlopen(req, data=data).read()
        response = response.decode('utf-8')
        return response
    except error.HTTPError as e:
        msg = e.read().decode('utf-8')
        print("sms_send_normal error:", msg)


def sms_send_iot(content, receiver):
    parameters = {'msisdns': [receiver], 'content': content}
    data = json.dumps(parameters).encode('utf-8')
    headers = {
                'Authorization': IoTAuthorization,
                'Content-Type': 'application/json'
    }
    req = request.Request(urlSendSmsIoT, headers=headers)
    try:
        response = request.urlopen(req, data=data).read()
        response = response.decode('utf-8')
        return response
    except error.HTTPError as e:
        msg = e.read().decode('utf-8')
        print("sms_send error:", msg)