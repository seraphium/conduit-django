from rest_framework.exceptions import ValidationError
import http
from urllib import request, parse, error

apiKey = "257b42a0e9a6d2f58fc9dcb176fa24da"
urlSendSmsYunpian = "https://sms.yunpian.com/v2/sms/single_send.json"


def sms_send(content, receiver):

    dataSendSms = "apikey=" + apiKey + "&mobile=" + receiver + "&text=" + content
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
        print("sms_send error:", msg)
