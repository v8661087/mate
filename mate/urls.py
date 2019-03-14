"""mate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from account import views
from django.conf import settings
from django.conf.urls.static import static
from images.views import image_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('explore/', image_list, name='image_list'),
    path('explore/people/suggested/', views.explore_people_suggested, name='people_suggested'),
    path('accounts/', include('account.urls')),
    path('', views.index, name='index'),
    path('<str:username>/', views.user_detail, name='user_detail'),
    path('<str:username>/channel', views.user_channel, name='user_channel'),
    path('<str:username>/saved', views.user_saved, name='user_saved'),
    path('<str:username>/tagged', views.user_tagged, name='user_tagged'),
    path('images/', include('images.urls', namespace='images')),
    path('user/follow/', views.user_follow, name='user_follow'),
    path('emails/settings/', views.emails_settings),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)