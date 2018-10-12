from django.core.management.base import BaseCommand #, commandError
from .voa import sendmail,get_data_new
import subprocess
import os,re
import datetime
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
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
                sendmail.send_mail() # send mail
                log = 'send mail success!'
            except:
                log = 'send mail fail!'
        else:
            log = 'there is no html files'
        with open('log.txt','w') as f:
            log += '---%s'%datetime.date.today()
            f.write(log)