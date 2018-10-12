# -*- coding:utf-8 -*-

from . import sendmail,get_data_new
import subprocess
import os,re
import datetime
import time
path = os.path.dirname(os.path.abspath(__file__))

def doit(order):
    try:
        job = subprocess.Popen(order,shell = True)
        job.wait()
    except:
        pass

def main():
    get_data_new.main() # download the voa news
    html_files =[i for i in os.listdir('%s/result'%(path)) if re.findall(r'html',i)]
    if html_files:
        order_makemobi = '%s/kindlegen %s/result/*.opf'%(path,path)
        doit(order_makemobi) # make mobi format ebook
        time.sleep(15) # 休眠15秒
        sendmail.send_mail() # send mail
        return 'send mail success!'
    else:
        return 'there is no html files'
if __name__ =='__main__':
    main()
