# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 12:13:13 2018

@author: Administrator
"""
import requests
from bs4 import BeautifulSoup
import pdfkit
import os
import logging


html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
    {content}
    </body>
    </html>
    """

def get_html(url):
    '''
    爬取网页函数
    '''
    try:
        r = requests.get(url)
        r.raise_for_status
        r.encoding = 'utf-8'
        
        return r.content
        
    except:
        print('网络连接错误')
        
def run(url):
    '''
    主函数
    '''
    htmls=[]
    #遍历拿到的每一个url，对每个url的内容再进行爬取
    for index,url in enumerate(parse_menu(url)):
        #解析每一个网页的内容
        html = parse_body(url)
        f_name = '.'.join([str(index),'html'])
        
        #先将每一个html页面写入文件
        if html:
            with open(f_name,'wb') as f:
                f.write(html)
            #将每个文件的名字放到列表中
            htmls.append(f_name)
        
    #开始转为pdf
    save_pdf(htmls)

def save_pdf(htmls):
    '''
    储存为pdf文件
    '''
    #指明wkhtmltopdf的安装位置
    path_wk = r'E:\python3\mytool\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf = path_wk)
    #为输出的pdf设置一些参数，详见https://pypi.python.org/pypi/pdfkit
    options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
    try:
        #开始转换文件
        pdfkit.from_file(htmls,'mypdf'+".pdf",options=options,configuration=config)
    except:
        print('写入pdf出错')
    finally:
        #将所有生成的html的临时文件删除
        for html in htmls:
            os.remove(html)
    
def parse_menu(url):
    '''
    解析目录结构,获取所有URL目录列表
    '''
    #获取整个网页
    html = get_html(url)
    soup = BeautifulSoup(html,'lxml')
    menu_tag = soup.find_all(class_="design")[0]
    #遍历每个标签，并拿到他们的链接地址
    for menu in menu_tag.find_all('a'):
       url = menu['href']
       if not url.startswith('http'):
           url = 'http://www.runoob.com/python3/'+url
       #返回当前url
       yield url
        
def parse_body(url):
    '''
    解析网页正文
    '''
    try:
        html = get_html(url)
        soup =BeautifulSoup(html,'lxml')
        body = soup.find_all('div',class_='article-body')[0]
        content =html_template.format(content=body)
        content = content.encode('utf-8')
        return content
    except Exception as e:
        logging.error('解析错误',exc_info=True)
        

if __name__ == '__main__':
    url = 'http://www.runoob.com/python3/python3-tutorial.html'
    run(url)
