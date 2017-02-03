from django.conf.urls import url
# from views import index, loginvalidate, registervalidate, success, logout, zipupdate, register, community, adoption, editprofile, updateprofile, profilepage, addpet, eventform, createevent
from . import views

urlpatterns = [
    url(r'^$', views.success, name='success'),
    url(r'^login', views.index),
    url(r'^loginvalidate$', views.loginvalidate, name='loginvalidate'),
    url(r'^registervalidate$', views.registervalidate, name='registervalidate'),
    url(r'^success$', views.success, name='success'),
    url(r'^register$', views.register, name='register'),
    url(r'^community$', views.community, name='community'),
    # url(r'^adoption$', adoption, name='adoption'),
    url(r'^eventform$', views.eventform, name='eventform'),
    url(r'^createevent$', views.createevent, name='createevent'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^zipupdate$', views.zipupdate, name='zipupdate'),
    url(r'^editprofile$', views.editprofile, name='editprofile'),
    url(r'^updateprofile$', views.updateprofile, name='updateprofile'),
    url(r'^profilepage$', views.profilepage, name='profilepage'),
    url(r'^addpet$', views.addpet, name='addpet'),
    url(r'^post$', views.post),
    url(r'^forumtopic$', views.forumtopic),
    url(r'^topic/(?P<post_id>\d+)$', views.topic),
    url(r'^comment/(?P<post_id>\d+)$', views.comment),
    url(r'^deletecomment/(?P<post_id>\d+)/(?P<comment_id>\d+)$', views.deletecomment),
    url(r'^deletepost/(?P<post_id>\d+)$', views.deletepost),
]
