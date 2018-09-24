# -*- coding:utf-8 -*-

from .import sendmail,get_data_new
import subprocess
import os,re
import datetime

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
today = str(datetime.date.today() - datetime.timedelta(days=1))

def doit(order):
    try:
        job = subprocess.Popen(order,shell = True)
        job.wait()
    except:
        pass

def main():
    get_data_new.main() # download the voa news
    html_files =[i for i in os.listdir('%sresult'%(path)) if re.findall(r'html',i)]
    if html_files:
        order_makemobi = './kindlegen %sresult/*.opf'%(path)
        doit(order_makemobi) # make mobi format ebook
        sendmail.send_mail() # send mail
        return 'send mail success!'
    else:
        return 'there is no html files'
if __name__ =='__main__':
    main()
