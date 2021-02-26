import os
import sys
import json
import urllib.request

def translator(sentence, target_lang):

    client_id = "JZfaE1xnvsQcMk_nSKX9" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "EpTGHh0Eua" # 개발자센터에서 발급받은 Client Secret 값

    encText = urllib.parse.quote(sentence)
    data = f'source=en&target={target_lang}&text=' + encText

    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)

    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    response = urllib.request.urlopen(request, data=data.encode("utf-8"))

    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        res = json.loads(response_body.decode('utf-8'))
        print('translate')
        return res['message']['result']['translatedText']

    else:
        print("Error Code:" + rescode)
