# 爬虫爬取简书最近文章和热门文章，并用Django REST framework 生成api
## 使用
### 安装依赖环境
pip instakk -r requirement.txt
### 进入虚拟环境
source venv/bin/active
### 在MySQL中创建jianshu数据库
create database jianshu;
### 同步数据库
python manage.py makemigrations
python manage.py migrate
### 爬取数据
python latest_jianshu_news.py
python hot_article.py
### 运行web服务
python manage.py runserver 0.0.0.0:8000
### 浏览器访问
http://ip:8000/jianshu
## 爬取数据
首先创建django项目，分析文章特征，创建数据库表结构，同步数据库，生成相应的表
hot_article.py为爬取热门文章的程序，并将数据插入数据库
latest_jianshu_news.py为爬取最近文章的数据，并将数据插入数据库
## restful api
通过Django REST framework 形成

