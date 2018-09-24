
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart,MIMEBase
import datetime
import smtplib
import os
import re
import email
path =os.path.dirname(os.path.abspath(__file__))
def send_mail():
    mailserver = 'box374.bluehost.com:465'
    sender = 'ljy@luckylinjiayuan.cn'
    receivers =[
            'mlabm1985@163.com',
            '18550348986@163.com',
            '308627993@qq.com',
            '874374721@qq.com',
            '47772637@qq.com',
            '542765129@qq.com',
            '176943251@qq.com',
            '331391128@qq.com',
            'jffeng_cloud@hotmail.com',
            'Frank_gao@bio-rad.com',
            'magica1998@icloud.com',
            'lulu991210@163.com',
            '84186586@qq.com',
            'songnaimei@gmail.com',
            '904361038@qq.com',
            'gaoran234@163.com',
            '465961255@qq.com',
            'worldbeaterma@my.com',
            '1186507531@qq.com',
            'abedino@163.com',
            'wl_0232@163.com',
            'qqcody@163.com',
            'yingxu99@hotmail.com',
            'liaobo19960618@foxmail.com',
            'zhuanzhuyonggan@163.com',
            'cf_data@163.com',
            'doun@163.com',
            'litianlun198809@163.com',
            'G_daxia@yahoo.com',
            'claudine_he@qq.com',
            'jokic_ho@126.com',
            ]
   # receivers = receivers[-1:]
    today = datetime.date.today()
    smtp_server = smtplib.SMTP_SSL(mailserver)
    smtp_server.login(sender,'samsung@00')
    main_msg = MIMEMultipart()# 构造MIMEMultipart对象做为根容器
    text_msg = MIMEText("%s voa news for learning english"%(today),'plain','utf-8')# 构造MIMEText对象做为邮件显示内容并附加到根容器
    main_msg.attach(text_msg)
    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)
    dir = os.path.join(path,'result')
    all_files = [i for i in os.listdir(dir) if re.findall(r'mobi|mp3',i)]
    for i in all_files:
        f_path = os.path.join(dir,i)
        with open(f_path,'rb') as f:
            data = f.read()
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(data)
        email.encoders.encode_base64(file_msg)
        basename = os.path.basename(i.strip())
        file_msg.add_header('Content-Disposition','attachment', filename = basename)
        main_msg.attach(file_msg)

    # 设置根容器属性
    main_msg['From'] = sender
    main_msg['Subject'] = "%s voa news"%(today)
    fullText = main_msg.as_string()
    # 用smtp发送邮件
    try:
        n=0
        while n  < len(receivers):
            smtp_server.sendmail(sender,receivers[n:n+10], fullText)
            n+=10
            print('send mail to %s success !'%n)
    finally:
        smtp_server.quit()

if __name__=='__main__':
    send_mail()
