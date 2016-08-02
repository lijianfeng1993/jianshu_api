# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.

class ArticleList(models.Model):
    '''
        文章概要信息
    '''
    article_id = models.CharField('ID', primary_key=True, max_length=100)
    article_title = models.CharField('文章标题', max_length = 100)
    article_url = models.URLField('文章URL')
    article_user = models.CharField('作者', max_length = 100)
    article_user_url = models.URLField('作者URL')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created', ]
    
    def __unicode__(self):
        return self.article_title

    def __str__(self):
        return self.article_title

class ArticleDetail(models.Model):
    '''
        文章详细信息
    '''
    image = models.URLField('图片URL')
    article_title = models.CharField('文章标题', max_length = 100)
    body = models.TextField('文章内容', null = True)
    time = models.CharField('发表时间', max_length = 100, null = True)
    views_count = models.CharField('阅读数', max_length = 100)
    public_comments_count = models.CharField('评论数',max_length = 100)
    likes_count = models.CharField('喜欢',max_length = 100)
    total_rewards_count = models.CharField('打赏',max_length = 100)
    created = models.DateTimeField('创建时间',auto_now_add = True)

    class Meta:
        ordering = ['-created']
    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title


class HotArticle(models.Model):
    '''
        热门文章
    '''
    article_id = models.CharField('ID', primary_key=True, max_length=100)
    article_title = models.CharField('文章标题', max_length = 100)
    article_url = models.URLField('文章URL')
    article_body = models.TextField('文章内容', null = True)
    article_user = models.CharField('作者', max_length = 100)
    article_user_url = models.URLField('作者URL')
    article_image = models.URLField('图片URL')
    article_time = models.CharField('发表时间', max_length = 100, null = True)
    created = models.DateTimeField('创建时间',auto_now_add = True)
   
    class Meta:
        ordering = ['-created']
    def __unicode__(self):
        return self.article_title
    def __str__(self):
        return self.article_title 
