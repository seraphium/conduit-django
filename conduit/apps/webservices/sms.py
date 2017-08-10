from rest_framework.exceptions import ValidationError
import http
import urllib.request

apiKey = "257b42a0e9a6d2f58fc9dcb176fa24da"
urlSendSmsYunpian = "https://sms.yunpian.com/v2/sms/single_send.json"


def sms_send(content, receiver):
    try:
        dataSendSms = "apikey=" + apiKey + "&mobile=" + receiver + "&text=" + content

    except Exception as e:
        raise ValidationError('upload image failed ', e)