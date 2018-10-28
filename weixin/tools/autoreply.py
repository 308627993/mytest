import xml.etree.ElementTree as ET
import jinja2
from . import get_media_id,get_xml
import re
import os,glob
from weixin import models

django_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = '%s/weixin/management/commands/voa/result'%django_root_path
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
            emails = emailRegex.findall(content.strip())
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
            elif 'ebooks' in content:
                import subprocess,sys
                #s= subprocess.Popen('which python3',shell=True,stdout=subprocess.PIPE)
                if 'public' in content:
                    remain_hours = subprocess.Popen('python3 /opt/app-root/src/manage.py public_kindle',shell=True,stdout=subprocess.PIPE)
                    message = '%s ,start make mobi format ebooks for public'%remain_hours
                elif 'private' in content:
                    subprocess.Popen('python3 /opt/app-root/src/manage.py private_kindle',shell=True)
                    message = 'start make mobi format ebooks for private'
            elif content == 'log':
                #message = '%s--%s'%(path, delete_or_show_file(path='%s/weixin/management/commands/voa'%django_root_path,filetypes=['*.txt','*.py'],action='show'))
                with open('%s/weixin/management/commands/voa/log.txt'%django_root_path,'r') as f:
                    message = f.read()
            elif content == 'mails':
                from weixin.models import Email
                message = 'mails total %s EA'%(len(Email.objects.all()))
            elif 'remove' in content:
                mails = emailRegex.findall(content.replace('remove','').strip())
                print(mails)
                if mails:
                    print(mails[0])
                    remove_mail = models.Email.objects.filter(user_email = mails[0])
                    print(remove_mail)
                    if len(remove_mail)==1:
                        print(remove_mail[0])
                        try:
                            remove_mail[0].delete()
                            message = '%s 成功从数据库中删除！'%mails[0]
                        except:
                            message = '%s 从数据库中删除失败，请联系管理员确认问题点！'%mails[0]
                    else:
                        message = '%s 不在数据库中，不需要删除！'%mails[0]
                else:
                    message = '请正确的输入你需要删除的邮箱！'
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
