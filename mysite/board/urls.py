from django.urls import path

from . import views 

app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('compose', views.compose, name='compose'),
    path('logout', views.logout_user, name='logout_user'),
]