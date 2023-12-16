"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from video import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('videos/<int:page>', views.index, name='index'),
    path('popular/', views.popular, name='popular'),
    path('history/', views.history, name='history'),
    path('videos/create/', views.create, name='create'),
    path('videos/update/<int:video_id>/', views.update, name='update'),
    path('videos/delete/<int:video_id>/', views.delete, name='delete'),
    path('videos/<int:video_id>/', views.show, name='show_video'),
    path('videos/like/<int:video_id>/', views.like_video, name='like_video'),
    path('videos/dislike/<int:video_id>/', views.dislike_video, name='dislike_video'),
    path('videos/comment/<int:video_id>/', views.add_comment, name='add_comment'),
    path('videos/comment/like/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('videos/comment/dislike/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
    path('channels/create/', views.create_channel, name='create_channel'),
    path('channels/update/<int:channel_id>/', views.update_channel, name='update_channel'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
