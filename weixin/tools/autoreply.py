import xml.etree.ElementTree as ET
import jinja2
from . import get_media_id,get_xml
import re
from weixin import models
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
            else:
                message = 'Email格式不正确，请再次输入！'
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
