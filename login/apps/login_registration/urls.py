from django.conf.urls import url
<<<<<<< HEAD
from views import index, loginvalidate, registervalidate, success, logout, register, community, adoption
=======
from views import index, loginvalidate, registervalidate, success, logout
from . import views
>>>>>>> sam
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^loginvalidate$', loginvalidate, name='loginvalidate'),
    url(r'^registervalidate$', registervalidate, name='registervalidate'),
    url(r'^success$', success, name='success'),
    url(r'^logout$', logout, name='logout'),
<<<<<<< HEAD
    url(r'^register$', register, name='register'),
    url(r'^community$', community, name='community'),
    url(r'^adoption$', adoption, name='adoption')
=======
>>>>>>> sam
]
