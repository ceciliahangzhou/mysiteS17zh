from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^(?P<course_no>\d+)/$', views.detail, name='detail'),
        #url(r'^base/$', views.base, name='base'),
        url(r'^topic_part1/$', views.topic_part1, name='topic_part1'),
        url(r'^topics/$', views.topics_view, name='topics'),
        url(r'^addtopic/$', views.addtopic, name='addtopic'),
        url(r'^topics/(?P<topic_id>\d+)/$', views.topicdetail, name='topicdetail'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        url(r'mycourses/',views.mycourses, name='mycourses')
        ]
