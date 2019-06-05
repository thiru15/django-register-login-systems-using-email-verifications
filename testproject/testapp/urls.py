from django.conf.urls import url
from testapp import views

app_name = 'testapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.register, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
        url(r'^user_login/$',views.user_login,name='user_login'),
        url(r'^user_logout/$',views.user_logout,name='user_logout'),
]
