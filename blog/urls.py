from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^posts/create/$$', views.create_posts, name='create'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.detail_posts, name='detail'),
    url(r'^$', views.list_posts, name='list'),
]
