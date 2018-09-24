#获取上传文件的media_ID
#群发图片的时候，必须使用该api提供的media_ID'''

from . import get_token
import requests

def get_media_id(path,type):
    img_url='https://api.weixin.qq.com/cgi-bin/media/upload'
    with open(path,'rb') as f:
        data ={'media':f}
        payload_img={'access_token':get_token.get_token(),'type':type}
        response = requests.post(url=img_url,params=payload_img,files=data)
        if type=='image':
            return eval(response.content)['media_id']
        elif type=='thumb':
            return eval(response.content)['thumb_media_id']