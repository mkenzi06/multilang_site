from django.urls import path, include
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.articles_list, name='articles_list'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('api/chatbot/', views.chatbot_view, name='chatbot_view'),
    path('search/', views.search_view, name='search_view')
    
]
