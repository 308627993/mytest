from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'', views.weixin_main, name='weixin_main'),
    #url('show', views.show, name='show'),
]
