"""jianshu_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from models import ArticleList,HotArticle
'''
# ----User start-----
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# ----User end-----
'''
# ----ArticleList start----
class ArticleListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArticleList
        fields = ('article_id', 'article_title', 'article_url', 'article_user', 'article_user_url', 'created')
    
class ArticleListViewSet(viewsets.ModelViewSet):
    queryset = ArticleList.objects.all().order_by("-created")[:20]
    serializer_class = ArticleListSerializer
# ----ArticleList end-----
    
#----HotArticle start-----
class HotArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HotArticle
        fields = ('article_id', 'article_title', 'article_url', 'article_body', 'article_user', 'article_user_url', 'article_image', 'article_time', 'created')
    
class HotArticleViewSet(viewsets.ModelViewSet):
    queryset = HotArticle.objects.all().order_by("-created")[:20]
    serializer_class = HotArticleSerializer
#----HotArticle  end-------


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'latest_article_list',ArticleListViewSet)
router.register(r'hot_article',HotArticleViewSet)

urlpatterns = [
    url(r'^',include(router.urls)),
]
