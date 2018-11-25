#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import urllib.request as uq
import re
import datetime
from lxml import etree
import datetime
import jinja2
import os,glob
import chardet
import requests
import traceback

path = os.path.dirname(os.path.abspath(__file__))
def get_today():
    return str(datetime.date.today() - datetime.timedelta(days=1))

def delete_file(path,filetypes):
    '''删除指定目录下的指定类型的文件'''
    files = []
    for filetype in filetypes:
        files += glob.glob(os.path.join(path,filetype))
    for file in files:
        os.remove(file)

def get_data_from_url(url):
    heads = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
    response = requests.get(url,headers=heads)
    data = response.content
    encoding_type = chardet.detect(data)['encoding']
    data = data.decode(encoding_type,errors='ignore')
    html = etree.HTML(data)
    return html

def download_img(url):
    pic = requests.get(url,timeout=50) #超时异常判断 5秒超时
    if pic.status_code == 200:
        file_name = "%s/image/"%(path)+str(hash(url))+".jpg" #拼接图片名
        #将图片存入本地
        fp = open(file_name,'wb')
        fp.write(pic.content) #写入图片
        fp.close()
        return len(pic.content)
    else:
        #print(pic.status_code)
        return 0

def format_opf_ncx(titles,image_names,subject):
    with open('%s/template/template.opf'%(path),'r',encoding='utf-8') as f:
        template_opf = f.read()
    opf_template = jinja2.Template(template_opf)
    with open('%s/template/template.ncx'%(path),'r',encoding='utf-8') as f:
        template_ncx = f.read()
    ncx_template = jinja2.Template(template_ncx)
    image_names = set(image_names)
    opf_rend = opf_template.render({ 'titles':titles,'today':'%s'%(get_today()),'which':subject,})
    ncx_rend = ncx_template.render({ 'titles':titles, })
    with open("%s/result/%s.opf"%(path,get_today()),'w',encoding='utf-8') as f:
        f.write(opf_rend)
    with open("%s/result/KUG.ncx"%(path),'w',encoding='utf-8') as f:
        f.write(ncx_rend)

class GetData():
    def __init__(self,kvs):
        delete_file('%s/result'%(path),['*.html','*.opf','*.ncx','*.mobi','*.mp3'])
        delete_file('%s/image'%(path),['*.jpg',])
        self.html = get_data_from_url(kvs['url'])
        self.links = set(self.html.xpath(kvs['links_xpath']))
        self.page_title_xpath = kvs['page_title_xpath']
        self.page_body_xpath = kvs['page_body_xpath']
        self.page_image_xpath = kvs['page_image_xpath']
        self.page_useless_xpath = kvs['page_useless_xpath']
        self.page_mp3_xpath = kvs['page_mp3_xpath']
        self.subject = kvs['subject']
        self.titles = []
        self.image_names=[]
        self.all_links = self.filter_links()

    def filter_links(self):
        '''
        根据url特点进行:
        -筛选:剔除不符合要求的url，可以通过re.findall('pattern'),用正则表达式进行筛选
        -修改：因为有些url是相对路径，需要改为完整的url路径，如 url = 'http://xxx.com' + url
        最终return 满足要求的url list
        '''
        full_links = ['https://learningenglish.voanews.com'+i for i in self.links]
        return full_links
    def filter_page(self,html):
        '''
        根据自己设定的规则进行判定，返回输入的html是否符合要求
        '''
        if get_today() in html.xpath('.//time/@datetime')[0]:
            return True
        else:
            return False
    def download_format_page(self,title,context):
        '''
        １.打开模板html，进行渲染title和内容
        2.然后对渲染的html的字符串对象转换为etree树状结构对象
        3.选择所有含有属性的节点
        4.删除所有节点的属性
        5.对etree结构的对象转换为字符串对象的html
        6.把css文件链接加入到html内容里面
        7.把html写入result文件夹内保存
        '''
        with open('%s/template/template.html'%(path),'r',encoding='utf-8') as f:
            template_html = f.read()
        html_template = jinja2.Template(template_html)
        words =re.findall(r'[a-zA-Z\']+',' '.join(etree.HTML(context).xpath('.//text()')))
        html_rend = html_template.render({ 'title':title,'page':context,'date':get_today(),'subject':self.subject,'len_words':len(words)})
        html_tree = etree.HTML(html_rend)
        node_list = html_tree.xpath(r'.//*[@*]')
        for node in node_list:
            for attrib in node.attrib:
                if attrib != 'src':
                    del node.attrib[attrib]
     #   words =re.findall(r'[a-zA-Z\']+?',' '.join(html_tree.xpath('.//text()')))
        print(len(words))
        html_rend = etree.tostring(html_tree)
        encode_type = chardet.detect(html_rend)['encoding']
        html_rend = html_rend.decode(encode_type,errors="ignore").replace('<head>','<head>\n <link rel="stylesheet" type="text/css" href="../template/style.css">')

        with open("%s/result/%s.html"%(path,title),'w',encoding='utf-8') as f_html:
            f_html.write(html_rend)
            self.titles.append(title)
    def remove_useless_node(self,story_body,page_useless_xpath):
        '''
        根据设定的不需要的xpath，删除内容中的不需要的节点
        '''
        useless_nodes = story_body.xpath(page_useless_xpath)
        if useless_nodes:
            for i in useless_nodes:
                i.getparent().remove(i)
    def download_format_image(self,story_body):
        '''
        1.把html 树对象转换为字符串
        2.通过图片地址的xpath　获取图片地址的List，并去除不需要的地址
        3.for循环：找出小图片地址并更换为大图片的地址，并更新图片地址list，替换html 里面的内容
        4.下载图片返回图片大小，如果图片大小大于９kb:图片名字＝图片url的哈西值，如果图片地址不在html里面，则添加到html上。并把图片名添加到图片名list里面。
        '''
        context = etree.tostring(story_body)
        encoding_type = chardet.detect(context)['encoding']
        context = context.decode(encoding_type,errors="ignore")
        src_links = list(set([i for i in story_body.xpath(self.page_image_xpath) if 'http' in i])) # get all image links
        if 'https://gdb.voanews.com/6AD44B97-4251-4D10-B871-C134BBFB39FA_w250_r1.jpg' in src_links:
            src_links.remove('https://gdb.voanews.com/6AD44B97-4251-4D10-B871-C134BBFB39FA_w250_r1.jpg')
        for i in range(len(src_links)):
            url = src_links[i]
            img_250 = re.findall(r'_w\d+_',url)[0] if re.findall(r'_w\d+_',url) else None
            if img_250:
                img_640 = re.sub(r'_w\d+_','_w640_',url)
                context = context.replace(url,img_640)
                src_links[i] = img_640
            if download_img(src_links[i])>9000:
                link_name=str(hash(src_links[i]))
                if src_links[i] not in context:
                    context = '<div><img src="%s"></img></div>'%(src_links[i]) + context
                context = context.replace(src_links[i],'../image/%s.jpg'%(link_name))
                self.image_names.append(link_name)
        return context
    def download_mp3(self,html,title):
        '''
        从HTML下载符合mp3 xpath　规则的mp3
        对下载的mp3进行保存，并命名为title
        '''
        mp3_url = html.xpath(self.page_mp3_xpath)[1]
        title = title.replace(' ','_')
       # title = re.sub(r'[^a-zA-Z0-9_.]','',title)
        with open('%s/result/%s.mp3'%(path,title),'wb') as f:
            f.write(requests.get(mp3_url).content)
    def get_page(self):
        for url in self.all_links:
            try:
                html = get_data_from_url(url)
                if self.filter_page(html):
                    title = html.xpath(self.page_title_xpath)[0].strip()
                    title = re.sub(r"[^a-zA-Z0-9_.' ]",'',title)
                    self.download_mp3(html,title)
                    story_body = html.xpath(self.page_body_xpath)[0]
                    self.remove_useless_node(story_body,self.page_useless_xpath)
                    context = self.download_format_image(story_body)
                    self.download_format_page(title,context)
            except Exception as e:
                print(e)
        #        traceback.print_exc()
                #sys.exit(1)
def main():
    titles = []
    image_names = []
    urls_list = [
                ('https://learningenglish.voanews.com/z/952','Read Listen and Learn'),
                ('https://learningenglish.voanews.com/z/3521','As It Is'),
                ('https://learningenglish.voanews.com/z/986','Arts and Culture'),
                ('https://learningenglish.voanews.com/z/1581','American Stories'),
                ('https://learningenglish.voanews.com/z/955','Health and Lifestyle'),
                ('https://learningenglish.voanews.com/z/979','U.S. History'),
                ('https://learningenglish.voanews.com/z/1579','Science and Technology'),
                ('https://learningenglish.voanews.com/z/4652',"What's Trending Today ?"),
                ('https://learningenglish.voanews.com/z/987','Words and Their Stories'),
                ('https://learningenglish.voanews.com/z/1689','Learning English Broadcast'),
                ('https://learningenglish.voanews.com/z/5091',"America's Presidents"),
                ]
    voa_kvs = {
    'url':'url',
    'links_xpath':'//div/ul/li/div/a[@class="img-wrap"]/@href',
    'page_title_xpath':'//*[@id="content"]//h1/text()',
    'page_body_xpath':'//*[@id="article-content"]/div[1]',
    'page_image_xpath':'//img/@src|//div/@data-src',
    'page_useless_xpath':'.//div[@class="news-app-promo"]|.//style|.//script|.//noscript|.//div[@class="wsw__embed"]/div[contains(@class,media-pholder)]',
    'page_mp3_xpath':'.//a[contains(@href,"mp3")]/@href',
    'subject':'level 1 voanews',
    }
    get_data_objs = []
    for url,subject in urls_list:
        voa_kvs_dict = {k:v for k,v in voa_kvs.items()}
        voa_kvs_dict['url'] = url
        voa_kvs_dict['subject'] = subject
        get_data_objs.append(GetData(voa_kvs_dict))
    all_urls = []
    for obj in get_data_objs:
        for link in obj.all_links:
            if link not in all_urls:
                all_urls.append(link)
            else:
                obj.all_links.remove(link)
                print('remove :',link)
        obj.get_page()
        titles += obj.titles
        image_names += obj.image_names
    titles = list(set(titles))
    image_names = list(set(image_names))
    format_opf_ncx(titles,image_names,subject='VOA learning english')
    # delete the mp3 which don't need
    mp3_files = glob.glob(os.path.join('%s/result'%(path),'*.mp3'))
    html_titles =[i.replace('.html','') for i in glob.glob(os.path.join('%s/result'%(path),'*.html'))]
    print('mp3_files :',mp3_files)
    useless_mp3_files = [i for i in mp3_files if i.replace('.mp3','') not in html_titles]
    print('useless_mp3_files :',useless_mp3_files)
    for file in useless_mp3_files:
        os.remove(file)
        print('remove',file)
if __name__ == '__main__':
    main()
