import requests
import json

TOKEN = "Aa123456!"
servers = requests.get('http://interview.vulcancyber.com:3000/servers',headers={'Authorization': f'{TOKEN}'})

def get_api(url, headers):
    res = None
    try:
        res = requests.get(url, headers)
        if res is None or res.status_code is None or res.status_code >= 300:
            raise Exception("request failed for url {url}".format(url=url))
        res = json.loads(res.content)
    except Exception as e:
        print(e)

    return res


print(get_api('http://interview.vulcancyber.com:3000/servers', headers={'Authorization': f'{TOKEN}'}))
