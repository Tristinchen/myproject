import time
import hmac
import hashlib
import requests
import json

def get_milliseconds():
    milliseconds = int(round(time.time() * 1000))
    return milliseconds

def get_refreshToken():

    refreshToken=''
    times=str(get_milliseconds())
    print(times)
    url='https://maden.myshopline.com/admin/oauth/token/refresh'
    secret = b"bc2e157b7a147b317ef177be14d4f844b10aec09"

    dig = hmac.new(secret, bytes(str(times), 'utf-8'), digestmod=hashlib.sha256).hexdigest()
    print(dig)
    payload = {}
    headers = {
        'appkey': 'fa8b862c4c4107ea9de797f074cf0c0c7192f9c6',
        'sign': dig,
        'timestamp': times,
        'Content-Type': 'application/json'
    }
    print(headers)

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    refreshToken=json.loads(response.text).get("data").get('accessToken')
    print("已获取到token:", refreshToken)

    return refreshToken
get_refreshToken()