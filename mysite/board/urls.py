from django.urls import path

from . import views 

app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('users/<int:user_id>', views.user, name='user'),
    path('posts/<int:post_id>', views.post, name='post'),
    path('compose', views.compose_post, name='compose_post'),
    path('logout', views.logout_user, name='logout'),
]