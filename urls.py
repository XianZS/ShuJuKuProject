"""
URL configuration for djpy project.

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
    1. Import to function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapi.views import hadoop, yuanshen, login, homepage, logout, add_user, myself, logs, shujuku, link
urlpatterns = [
    path('admin', admin.site.urls),
    path('login', login.login),
    path('logout', logout.logout),
    path('', homepage.HomePage),
    path('search', homepage.search),
    path('bottom/outlook', link.outlook),
    path('bottom/news', link.news),
    path('bottom/about', link.about),
    path('myself', myself.myself),
    path('XiuGai_myself', myself.XiuGai),
    path('logs', logs.logs),
    path('shujuku/home', shujuku.find),
    path('shujuku/home/buy', shujuku.buys),
    path('shujuku/home/userthings', shujuku.userthings),
    path('shujuku/home/delete', shujuku.deletecar),
    path('shujuku/home/notice', shujuku.noticepage),
    path('shujuku/home/things', shujuku.thingspage),
    path('shujuku/home/logs', shujuku.logs),
]
handler404 = 'webapi.views.re404.page_not_found'
