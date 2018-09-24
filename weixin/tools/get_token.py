from django.core.cache import cache
import requests

def get_token():
    if cache.get('token'):
        return cache.get('token')
    else:
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxecf00ceac96fa4ac&secret=a23adbe6a48cd3e57fd843c3e6be5223'
        response = requests.get(url)
        if response.status_code == 200:
            token = eval(response.content)['access_token']
            cache.set('token', token)
            return token