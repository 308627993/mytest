from django.core.management.base import BaseCommand #, commandError
from .voa import sendmail,get_data_new
import subprocess
import os,re
import datetime
import time
import threading
from weixin.models import Email

class Command(BaseCommand):
    def handle(self, *args, **options):
        def everyday_job():
            path = os.path.dirname(os.path.abspath(__file__))
            def doit(order):
                try:
                    job = subprocess.Popen(order,shell = True)
                    job.wait()
                except:
                    pass
            get_data_new.main() # download the voa news
            html_files =[i for i in os.listdir('%s/voa/result'%(path)) if re.findall(r'html',i)]
            log = ''
            if html_files:
                try:
                    order_makemobi = '%s/voa/kindlegen %s/voa/result/*.opf'%(path,path)
                    doit(order_makemobi) # make mobi format ebook
                    time.sleep(15) # 休眠15秒
                    mail_list = [i.user_email for i in Email.objects.all()]
                    n=0
                    while n<len(mail_list):
                        sendmail.send_mail(mail_list[n:n+74]) # send mail
                        n+=74
                        time.sleep(3700) # 休眠30秒,保证每３０秒发送１封邮件，１封邮件收件人１００人
                    log += 'send mail public success!'
                except Exception as e:#, Argment:
                    log += 'send mail fail! Exception:%s'%e
            else:
                log += 'there is no html files,can not make mobi file'
            with open('%s/voa/log.txt'%path,'w') as f:
                log += '---%s'%datetime.datetime.now()
                print(log)
                f.write(log)
            def remain_seconds():
                tomorrow = (datetime.date.today()+datetime.timedelta(days=1))
                return (datetime.datetime(tomorrow.year,tomorrow.month,tomorrow.day,9,10)-datetime.datetime.now()).total_seconds()
            timer = threading.Timer(remain_seconds(),everyday_job) #每天执行一次
            timer.start()
        everyday_job()
