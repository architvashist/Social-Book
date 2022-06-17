from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('follow',views.follow,name='follow'),
    path('search',views.search,name='search'),
    path('like_post',views.like_post,name='like_post'),
    path('upload',views.upload,name='upload'),
    path('settings',views.settings,name='settings'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('logout',views.logout_user,name='logout'),
]