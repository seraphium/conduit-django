from rest_framework.exceptions import ValidationError
import http, json
from urllib import request, parse, error
from conduit.apps.units.models import Unit

yunpianApiKey = "257b42a0e9a6d2f58fc9dcb176fa24da"
urlSendSmsYunpian = "https://sms.yunpian.com/v2/sms/single_send.json"
urlSendSmsIoT = 'http://120.26.213.169/api/sms/'
urlGetAuthIoT = "http://120.26.213.169/api/access_token/"
IoTToken = ""

urlGetWeatherCodeTemplate = "http://restapi.amap.com/v3/config/district?key=b16dc715445f887cd759850793a5b163&keywords={0}&subdistrict=0&showbiz=false&extensions=base"
urlGetWeatherTemplate = "http://restapi.amap.com/v3/weather/weatherInfo?key=b16dc715445f887cd759850793a5b163&city={0}"

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

def get_auth_iot():
    global IoTToken

    headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = "username=bshbkjd&password=123123".encode('utf-8')
    req = request.Request(urlGetAuthIoT, headers=headers)

    response = request.urlopen(req, data=data).read()
    response = response.decode('utf-8')
    resp = json.loads(response)
    if resp['code'] == 200:
        IoTToken = 'JWT ' + resp['token']


def sms_send_iot(content, receiver):
    parameters = {'msisdns': [receiver], 'content': content}
    data = json.dumps(parameters).encode('utf-8')
    get_auth_iot()
    headers = {
                'Authorization': IoTToken,
                'Content-Type': 'application/json'
    }
    req = request.Request(urlSendSmsIoT, headers=headers)
    try:
        response = request.urlopen(req, data=data).read()
        response = response.decode('utf-8')
        resp = json.loads(response)
        print("sms_respnse:", resp)

        if resp['code'] == 200:
            return ""
        else:
            return resp['msg']
    except error.HTTPError as e:
        msg = e.read().decode('utf-8')
        print("sms_send error:", msg)
        return resp['msg']

def unitGetWeather(unit):
    code = 0
    urlGetWeatherCode = urlGetWeatherCodeTemplate.format(parse.quote(unit['city']))
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    req = request.Request(urlGetWeatherCode, headers=headers)
    try:
        resp = request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp)
        code = resp['districts'][0]['adcode']
    except error as e:
        msg = e.read().decode('utf-8')
        print("unit get weather code error:", msg)
    urlGetWeather = urlGetWeatherTemplate.format(code)
    req = request.Request(urlGetWeather, headers=headers)
    try:
        resp = request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp)
        weather = resp["lives"][0]["weather"]
        print(weather)
    except error as e:
        msg = e.read().decode('utf-8')
        print("unit get weather error:", msg)


    return weather