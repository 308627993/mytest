import xml.etree.ElementTree as ET
import jinja2
from . import get_media_id,get_xml
import re
import os,glob
from weixin import models


path = '%s/voa/tools/result'%(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def delete_or_show_file(path,filetypes,action):
    '''删除指定目录下的指定类型的文件'''
    files = []
    for filetype in filetypes:
        files += glob.glob(os.path.join(path,filetype))
    if action == 'show':
        print(files)
        return str(files)
    elif action == 'delete':
        for file in files:
            os.remove(file)



def autoreply(request):
    try:
        webData = request.body
        xmlData = ET.fromstring(webData)
        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text
        toUser = FromUserName
        fromUser = ToUserName
        if msg_type == 'text':
            xml = get_xml.get_xml('text')
            xml_template = jinja2.Template(xml)
            content = xmlData.find('Content').text
            emailRegex = re.compile(r"^[-\w\.]{1,63}@[-\w]{2,63}\.[a-zA-Z]{2,6}$")
            emails = emailRegex.findall(content)
            if emails:
                email = emails[0]
                if models.Email.objects.filter(user_email=email):
                    message = '该Email已经存在，添加时间[%s]'%(str(models.Email.objects.get(user_email=email).create_time)[:19])
                else:
                    models.Email.objects.create(user_email = email,user_id = FromUserName)
                    message = 'Email成功添加，保存时间[%s]'%(str(models.Email.objects.get(user_email=email).create_time)[:19])
            elif content == 'show':
                message = '%s--%s'%(path, delete_or_show_file(path=path,filetypes=['*.htm','*.html','*.mp3','*.mobi'],action='show'))
            elif content == 'delete':
                delete_or_show_file(path=path,filetypes=['*.html','*.mp3','*.mobi'],action='delete')
            elif content == 'ebooks':
                import subprocess
                message = 'make mobi file and send mail start...'
                #from voa.tools import mykindle
                #mykindle.main()
                subprocess.Popen(['python','../../../voa/tools/mykindle.py'],shell=True)
            elif content == 'mails':
                from weixin.models import Email
                message = 'mails total %s EA'%(len(Email.objects.all()))
            else:
                message = '%s不是正确的Email格式，请再次输入！'%content
            text_dict = {
                'toUser':toUser,
                'fromUser':fromUser,
                'createTime':CreateTime,
                'type':'text',
                'content':message,
                }
            context = xml_template.render(text_dict)
            return context

    except Exception as e:#, Argment:
        return e# Argment
