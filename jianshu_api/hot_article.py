#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''
    爬取简书新上榜的文章（首页20篇）
'''

__author__ = 'lijianfeng'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import requests
import MySQLdb
import time
from collections import OrderedDict
from colorama import init,Fore
from jianshu_api.settings import DATABASES


def get_page_url(base_url,domain_url):
    '''
        获取下一页的url
    '''
    html = requests.get(base_url).content
    soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    result = soup.find_all('button',class_ = 'ladda-button')
    if result:
        for url in result:
            data_url = url['data-url']
        data_url = domain_name + data_url
        return data_url
    else:
        return 0

def get_details(mysql, page,base_url, domain_name, article_table):
    '''
        爬取文章并获取详细信息
    '''
    article_list = OrderedDict()
    html = requests.get(base_url).content

    # html是网页源码，soup是获得一个对象
    soup = BeautifulSoup(html,'html.parser', from_encoding='utf-8')
    tags = soup.find_all('li',class_ = 'have-img')
    print Fore.YELLOW + 'page:%s-------------articles:%s---------------:' % (page,len(tags))
    global ct 
    
    # 对每篇文章处理
    for tag in tags:
        article_image = tag.img['src'].split('?')[0]
        article_user = tag.p.a.get_text()
        
        article_user_url = tag.p.a['href']
        if article_user_url.startswith('/users/'):
            article_user_url = domain_name + article_user_url
        
        created = tag.p.span['data-shared-at']
        article_title = tag.h4.get_text(strip = True)
        article_title = article_title.replace('"','\\"')
        article_url = tag.h4.a['href']
        article_id = article_url.split('/')[2]
        
        if article_url.startswith('/p/'):
            article_url = domain_name + article_url
    
        article_body = get_body(article_url)
        article_time = mysql.get_current_time()
        
        article_list['article_id'] = article_id
        article_list['article_title'] = article_title
        article_list['article_url'] = article_url
        article_list['article_user'] = article_user
        article_list['article_user_url'] = article_user_url
        article_list['article_body'] = article_body
        article_list['article_image'] = article_image
        article_list['created'] = created
        article_list['article_time'] = article_time
        
        
        print Fore.YELLOW + '-------开始插入第%s条数据------' % ct
        #for key,values in article_list.items():
            #print key+':'+values
        print '文章标题：' + article_list['article_title']
        result = mysql.insert_data(article_table,article_list)
        if result:
            print Fore.GREEN + 'article_table:数据保存成功！'
        else:
            print Fore.RED + 'article__table:数据保存失败！'
        ct = ct+1
        
    data_url = get_page_url(base_url,domain_name)
    if data_url:
        page = data_url.split('&')[-1]
        page = page.split('=')[1]
        get_details(mysql, page, data_url, domain_name, article_table)
        
    else:
        print Fore.GREEN + '-----------简书中热门文章以爬取完毕，共有%s篇----' % ct
        return 


def get_body(article_url):
    '''
        获取文章内容
    '''
    html = requests.get(article_url).content
    soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    tags = soup('div',class_ = 'show-content' )
    body = str(tags[0])
    
    body = body.replace('"','\\"')
    body = body.replace("'","\\'")
    return body


class Mysql(object):
    def get_current_time(self):
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return create_time
    
    def __init__(self,host,user,passwd,db,port):
        try:
            self.conn = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db, port = port, charset = 'utf8')
            self.cur = self.conn.cursor()
        except MySQLdb.Error as e:
            print Fore.RED +'连接数据库失败'
            print Fore.RED + self.get_current_time()
    
    def insert_data(self,table,my_dict):
        try:
            keys = ','.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            values = '"' + values + '"'
            try:
                sql = "insert into %s (%s) values(%s)" % (table, keys, values)
                result = self.cur.execute(sql)
                self.conn.commit()
                if result:
                    return 1
                else:
                    return 0
            except MySQLdb.Error as e:
                self.conn.rollback()
                if "key 'PRIMARY'" in e.args[1]:
                    print Fore.RED + self.get_current_time(),'数据已存在，未插入数据'
                else:
                    print Fore.RED + self.get_current_time(),'插入数据错误，原因%d: %s' % (e.args[0],e.args[1])
    
        except MySQLdb.Error as e:
            print Fore.Red + self.get_current_time(),'数据库错误，原因%d: %s' % (e.args[0],e.args[1])
 



if __name__ == '__main__':
    ct = 1
    host = DATABASES['default']['HOST']
    user = DATABASES['default']['USER']
    passwd = DATABASES['default']['PASSWORD']
    db = DATABASES['default']['NAME']
    port = DATABASES['default']['PORT']

    # 保存文章的表，由django创建好了
    article_table = 'jianshu_hotarticle'

    # 通过使用autoreset参数可以让变色效果只对当前输出有效，输出完成后颜色回复默认设置
    init(autoreset = True)
    
    domain_name = 'http://www.jianshu.com'
    base_url = 'http://www.jianshu.com'
    
    mysql = Mysql(host, user, passwd, db, port)
    page = 1
    get_details(mysql,page, base_url, domain_name, article_table)


    



